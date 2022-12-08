# coding: utf-8

from typing import Optional, Dict

import concepts
import db


def get_repositories() -> list[concepts.Repository]:
    """Get all repositories recorded.

    Returns:
        Repository list.
    """
    sess = db.get_session()
    repositories: list[db.Repository] = sess.query(db.Repository).all()
    result: list[concepts.Repository] = []
    for repository in repositories:
        result.append(concepts.Repository(repository.name, repository.path, repository.id))
    return result


def get_repository_by_id(repository_id: int) -> Optional[concepts.Repository]:
    sess = db.get_session()
    repository = sess.query(db.Repository).filter(db.Repository.id == repository_id).first()
    return repository


def get_repositories_by_name(name: str) -> list[concepts.Repository]:
    return []


def create_repository(repository: concepts.Repository):
    """Create repository instance.

    Args:
        repository: Repository information.

    Returns:
    """
    repo = db.Repository(name=repository.name, path=repository.path)
    sess = db.get_session()
    sess.add(repo)
    sess.commit()


def delete_repository(repository_id: int) -> None:
    sess = db.get_session()
    repo = sess.query(db.Repository).filter(db.Repository.id == repository_id).first()
    if isinstance(repo, db.Repository):
        sess.delete(repo)
        sess.commit()


def update_repository(repository: concepts.Repository) -> None:
    sess = db.get_session()
    repo = sess.query(db.Repository).filter(db.Repository.id == repository.id).first()
    if isinstance(repo, db.Repository):
        repo.name = repository.name
        repo.path = repository.path
        sess.commit()


def get_repository_directories(repo: concepts.Repository) -> Dict[str, str]:
    result = {
        "solution": "",
        "debug": "",
        "release": "",
        "qdebug": "",
    }
    if isinstance(repo, concepts.Repository):
        root: str = repo.path
        if len(root) != 0:
            result["solution"] = f"{root}\\bin\\X64BuildProject"
            result["debug"] = f"{root}\\bin\\x64Debug"
            result["release"] = f"{root}\\bin\\x64Release"
            result["qdebug"] = f"{root}\\bin\\x64Q_Debug"
    return result
