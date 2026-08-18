"""Contract for the post-render cover stage shared by production pipelines."""

from pathlib import Path

from lib.pipeline_loader import get_stage_order, list_pipelines, load_pipeline


NON_PRODUCTION_MANIFESTS = {"framework-smoke"}


def test_every_production_pipeline_generates_a_cover_after_compose():
    for pipeline_name in list_pipelines():
        if pipeline_name in NON_PRODUCTION_MANIFESTS:
            continue

        manifest = load_pipeline(pipeline_name)
        if manifest.get("deliverable_type", "video") != "video":
            continue
        order = get_stage_order(manifest)
        assert "compose" in order, pipeline_name
        compose_index = order.index("compose")
        assert order[compose_index + 1] == "cover", pipeline_name

        cover = manifest["stages"][compose_index + 1]
        assert cover["skill"] == "pipelines/shared/cover-director", pipeline_name
        assert cover["required_artifacts_in"] == ["render_report"], pipeline_name
        assert "cover_package" in cover["produces"], pipeline_name
        assert cover["checkpoint_required"] is True, pipeline_name
        assert cover["human_approval_default"] is True, pipeline_name


def test_publish_requires_the_approved_cover_when_present():
    for pipeline_name in list_pipelines():
        if pipeline_name in NON_PRODUCTION_MANIFESTS:
            continue

        manifest = load_pipeline(pipeline_name)
        if manifest.get("deliverable_type", "video") != "video":
            continue
        stages = {stage["name"]: stage for stage in manifest["stages"]}
        if "publish" not in stages:
            continue
        assert "cover_package" in stages["publish"]["required_artifacts_in"], pipeline_name


def test_shared_cover_director_exists():
    root = Path(__file__).resolve().parents[2]
    assert (root / "skills/pipelines/shared/cover-director.md").is_file()
