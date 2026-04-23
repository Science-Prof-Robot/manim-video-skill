"""
Manim Project Versioning System
Git-based version control for Manim animation projects
"""

import os
import json
import shutil
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict


def _default_scene_class_name(scene_name: str) -> str:
    """Map a scene slug to a Manim class name (e.g. scene_1 -> Scene1, intro -> Intro)."""
    parts = scene_name.replace("-", "_").split("_")
    return "".join(p.capitalize() for p in parts if p)


class ManimProject:
    """Git-versioned Manim animation project manager"""
    
    def __init__(self, name: str, base_path: Optional[str] = None):
        self.name = name
        self.base_path = Path(base_path) if base_path else Path.cwd()
        self.project_path = self.base_path / name
        self.scenes_path = self.project_path / "scenes"
        self.media_path = self.project_path / "media"
        self.config_path = self.project_path / "project.json"
        
    def init(self) -> None:
        """Initialize project with git repository and folder structure"""
        # Create directories
        self.project_path.mkdir(parents=True, exist_ok=True)
        self.scenes_path.mkdir(exist_ok=True)
        self.media_path.mkdir(exist_ok=True)
        (self.scenes_path / "shared").mkdir(exist_ok=True)
        
        # Initialize git repo
        if not (self.project_path / ".git").exists():
            self._git("init")
            self._git("config", "user.email", "manim@localhost")
            self._git("config", "user.name", "Manim Animation")
        
        # Create project config
        config = {
            "name": self.name,
            "created": datetime.now().isoformat(),
            "scenes": {},
            "version": "1.0"
        }
        self._save_config(config)
        
        # Initial commit
        self._git("add", ".")
        self._git("commit", "-m", "Initial project setup", "--allow-empty")
        
        print(f"✓ Project '{self.name}' initialized at {self.project_path}")
    
    def create_scene(self, scene_name: str, code: str, 
                     description: str = "") -> None:
        """Create a new scene with initial code"""
        scene_path = self.scenes_path / scene_name
        scene_path.mkdir(exist_ok=True)
        (scene_path / "versions").mkdir(exist_ok=True)
        (scene_path / "branches").mkdir(exist_ok=True)
        
        # Write initial scene file
        scene_file = scene_path / f"{scene_name}.py"
        scene_file.write_text(code)
        
        # Update config
        config = self._load_config()
        config["scenes"][scene_name] = {
            "created": datetime.now().isoformat(),
            "current_version": 1,
            "description": description,
            "branches": []
        }
        self._save_config(config)
        
        # Commit
        self._git("add", ".")
        self._git("commit", "-m", f"{scene_name} v1: initial creation")
        
        # Save immutable v1 copy
        shutil.copy(scene_file, scene_path / "versions" / "v1.py")
        
        print(f"✓ Scene '{scene_name}' created (v1)")
    
    def update_scene(self, scene_name: str, code: str, 
                     branch: Optional[str] = None) -> None:
        """Update scene code (creates new version on main or specified branch)"""
        scene_path = self._get_scene_path(scene_name, branch)
        scene_file = scene_path / f"{scene_name}.py"
        
        # Write updated code
        scene_file.write_text(code)
        
        # If on branch, just save - no version increment
        if branch:
            print(f"✓ Scene '{scene_name}' updated on branch '{branch}'")
            return
        
        # On main: increment version
        config = self._load_config()
        current = config["scenes"][scene_name]["current_version"]
        new_version = current + 1
        config["scenes"][scene_name]["current_version"] = new_version
        config["scenes"][scene_name]["updated"] = datetime.now().isoformat()
        self._save_config(config)
        
        # Commit
        self._git("add", ".")
        self._git("commit", "-m", f"{scene_name} v{new_version}: update")
        
        # Save immutable copy
        shutil.copy(scene_file, self.scenes_path / scene_name / "versions" / f"v{new_version}.py")
        
        print(f"✓ Scene '{scene_name}' updated (v{new_version})")
    
    def render(
        self,
        scene_name: str,
        branch: Optional[str] = None,
        quality: str = "medium",
        auto_commit: bool = True,
        scene_class: Optional[str] = None,
    ) -> str:
        """Render scene and optionally commit.

        scene_class: Manim scene class name inside the file. If omitted, derived from
        scene_name (scene_1 -> Scene1). Override when your class name does not match.
        """
        scene_path = self._get_scene_path(scene_name, branch)
        scene_file = scene_path / f"{scene_name}.py"
        
        if not scene_file.exists():
            raise FileNotFoundError(f"Scene file not found: {scene_file}")
        
        # Determine quality flags
        quality_flag = {"low": "-ql", "medium": "-qm", "high": "-qh"}.get(quality, "-qm")
        
        cls = scene_class or _default_scene_class_name(scene_name)
        # Manim CLI requires the scene class name after the file path.
        cmd = ["manim", quality_flag, str(scene_file), cls, "--disable_caching"]
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=self.project_path)
        
        if result.returncode != 0:
            print(f"Render error: {result.stderr}")
            raise RuntimeError(f"Render failed for {scene_name}")
        
        # Find output file
        output_dir = self.project_path / "media" / "videos" / scene_name
        if quality == "high":
            output_dir = output_dir / "1080p60"
        elif quality == "medium":
            output_dir = output_dir / "720p30"
        else:
            output_dir = output_dir / "480p15"
        
        # Get the mp4 file
        mp4_files = list(output_dir.glob("*.mp4"))
        if not mp4_files:
            raise FileNotFoundError("No output video found")
        
        source_video = mp4_files[0]
        
        # Copy to media with version tag
        config = self._load_config()
        version = config["scenes"][scene_name]["current_version"]
        branch_tag = f"_{branch}" if branch else ""
        dest_name = f"{scene_name}{branch_tag}_v{version}.mp4"
        dest_path = self.media_path / dest_name
        
        shutil.copy(source_video, dest_path)
        
        # Create symlink to latest
        latest_link = self.media_path / f"{scene_name}{branch_tag}_latest.mp4"
        if latest_link.exists() or latest_link.is_symlink():
            latest_link.unlink()
        latest_link.symlink_to(dest_path)
        
        # Auto-commit if on main
        if auto_commit and not branch:
            self._git("add", ".")
            self._git("commit", "-m", f"{scene_name} v{version}: render", "--allow-empty")
        
        print(f"✓ Rendered: {dest_path}")
        return str(dest_path)
    
    def versions(self, scene_name: str) -> List[Dict]:
        """List all versions of a scene"""
        scene_path = self.scenes_path / scene_name
        versions_dir = scene_path / "versions"
        
        if not versions_dir.exists():
            return []
        
        versions = []
        for vfile in sorted(versions_dir.glob("v*.py")):
            version_num = int(vfile.stem[1:])  # v1.py -> 1
            stat = vfile.stat()
            versions.append({
                "version": version_num,
                "file": str(vfile),
                "created": datetime.fromtimestamp(stat.st_mtime).isoformat()
            })
        
        return versions
    
    def rollback(self, scene_name: str, version: int) -> None:
        """Restore scene to specific version"""
        scene_path = self.scenes_path / scene_name
        version_file = scene_path / "versions" / f"v{version}.py"
        scene_file = scene_path / f"{scene_name}.py"
        
        if not version_file.exists():
            raise FileNotFoundError(f"Version {version} not found")
        
        # Restore code
        shutil.copy(version_file, scene_file)
        
        # Update config
        config = self._load_config()
        config["scenes"][scene_name]["current_version"] = version
        config["scenes"][scene_name]["rolled_back"] = datetime.now().isoformat()
        self._save_config(config)
        
        # Commit rollback
        self._git("add", ".")
        self._git("commit", "-m", f"{scene_name}: rollback to v{version}")
        
        print(f"✓ Rolled back '{scene_name}' to v{version}")
    
    def branch(self, scene_name: str, branch_name: str) -> None:
        """Create a provisional branch for a scene"""
        scene_path = self.scenes_path / scene_name
        branches_dir = scene_path / "branches" / branch_name
        branches_dir.mkdir(parents=True, exist_ok=True)
        
        # Copy current scene to branch
        scene_file = scene_path / f"{scene_name}.py"
        branch_file = branches_dir / f"{scene_name}.py"
        shutil.copy(scene_file, branch_file)
        
        # Update config
        config = self._load_config()
        if branch_name not in config["scenes"][scene_name]["branches"]:
            config["scenes"][scene_name]["branches"].append(branch_name)
        self._save_config(config)
        
        print(f"✓ Branch '{branch_name}' created for '{scene_name}'")
    
    def merge(self, scene_name: str, branch_name: str) -> None:
        """Merge branch into main, creating new version"""
        scene_path = self.scenes_path / scene_name
        branch_file = scene_path / "branches" / branch_name / f"{scene_name}.py"
        scene_file = scene_path / f"{scene_name}.py"
        
        if not branch_file.exists():
            raise FileNotFoundError(f"Branch '{branch_name}' not found")
        
        # Copy branch code to main
        shutil.copy(branch_file, scene_file)
        
        # Increment version
        config = self._load_config()
        current = config["scenes"][scene_name]["current_version"]
        new_version = current + 1
        config["scenes"][scene_name]["current_version"] = new_version
        config["scenes"][scene_name]["merged_from"] = branch_name
        self._save_config(config)
        
        # Commit
        self._git("add", ".")
        self._git("commit", "-m", f"{scene_name} v{new_version}: merged from {branch_name}")
        
        # Save version copy
        shutil.copy(scene_file, scene_path / "versions" / f"v{new_version}.py")
        
        print(f"✓ Merged '{branch_name}' into '{scene_name}' (v{new_version})")
    
    def delete_branch(self, scene_name: str, branch_name: str) -> None:
        """Delete a provisional branch"""
        branch_path = self.scenes_path / scene_name / "branches" / branch_name
        
        if branch_path.exists():
            shutil.rmtree(branch_path)
        
        # Update config
        config = self._load_config()
        if branch_name in config["scenes"][scene_name]["branches"]:
            config["scenes"][scene_name]["branches"].remove(branch_name)
        self._save_config(config)
        
        print(f"✓ Branch '{branch_name}' deleted")
    
    def tag(self, scene_name: str, version: int, tag: str) -> None:
        """Tag a specific version (e.g., 'approved', 'final')"""
        config = self._load_config()
        
        if "tags" not in config["scenes"][scene_name]:
            config["scenes"][scene_name]["tags"] = {}
        
        config["scenes"][scene_name]["tags"][tag] = version
        self._save_config(config)
        
        # Git tag
        tag_name = f"{scene_name}-v{version}-{tag}"
        self._git("tag", "-f", tag_name)
        
        print(f"✓ Tagged {scene_name} v{version} as '{tag}'")
    
    def diff(self, scene_name: str, v1: int, v2: int) -> str:
        """Show diff between two versions"""
        scene_path = self.scenes_path / scene_name
        file1 = scene_path / "versions" / f"v{v1}.py"
        file2 = scene_path / "versions" / f"v{v2}.py"
        
        result = subprocess.run(
            ["diff", "-u", str(file1), str(file2)],
            capture_output=True, text=True
        )
        
        return result.stdout if result.stdout else "No differences"
    
    def _get_scene_path(self, scene_name: str, branch: Optional[str] = None) -> Path:
        """Get path to scene (main or branch)"""
        if branch:
            return self.scenes_path / scene_name / "branches" / branch
        return self.scenes_path / scene_name
    
    def _load_config(self) -> Dict:
        """Load project configuration"""
        if self.config_path.exists():
            return json.loads(self.config_path.read_text())
        return {"scenes": {}}
    
    def _save_config(self, config: Dict) -> None:
        """Save project configuration"""
        self.config_path.write_text(json.dumps(config, indent=2))
    
    def _git(self, *args) -> subprocess.CompletedProcess:
        """Run git command in project directory"""
        return subprocess.run(
            ["git"] + list(args),
            cwd=self.project_path,
            capture_output=True
        )


# Convenience functions for direct use
def init_project(name: str, path: Optional[str] = None) -> ManimProject:
    """Initialize a new Manim project with versioning"""
    project = ManimProject(name, path)
    project.init()
    return project


def quick_render(scene_file: str, scene_class: str, quality: str = "medium") -> str:
    """Quick render without versioning (for testing)"""
    quality_flag = {"low": "-ql", "medium": "-qm", "high": "-qh"}.get(quality, "-qm")
    
    cmd = ["manim", quality_flag, scene_file, scene_class, "--disable_caching"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        raise RuntimeError(f"Render failed: {result.stderr}")
    
    # Find output
    scene_name = Path(scene_file).stem
    output_dir = Path("media") / "videos" / scene_name
    
    if quality == "high":
        output_dir = output_dir / "1080p60"
    elif quality == "medium":
        output_dir = output_dir / "720p30"
    else:
        output_dir = output_dir / "480p15"
    
    mp4_files = list(output_dir.glob("*.mp4"))
    return str(mp4_files[0]) if mp4_files else ""
