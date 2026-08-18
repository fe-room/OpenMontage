# Packaging Director — Finance WeChat Article

## Objective

Assemble the approved article and visuals into a local manual-publication bundle.
Produce `wechat_article_package` with `wechat_article_bundle`.

## Process

1. Verify the approved draft Markdown, cover, and every ordered figure exist.
2. Build `source_notes` from the research bibliography, including dates, scope,
   and any local data-file references.
3. Complete every checklist field honestly. A false item produces
   `status: needs_revision`; do not relabel it ready.
4. Call `wechat_article_bundle` with output directory
   `projects/<id>/deliverables/wechat/`.
5. Open the resulting manifest and verify paths remain inside the project.
6. Report the local bundle as ready or needs revision. Do not call any browser,
   account, upload, remote-draft, or publication action.

## Expected Bundle

```text
deliverables/wechat/
  article.md
  sources.md
  manifest.json
  images/
    cover.png
    01-...
    02-...
```

## Quality Checklist

- [ ] Package artifact validates and exact disclaimer remains intact.
- [ ] Figure order matches the approved article.
- [ ] Source notes are usable during fact-checking.
- [ ] `manual_publish_required` is true.
- [ ] User receives the bundle path, not a false “published” status.
