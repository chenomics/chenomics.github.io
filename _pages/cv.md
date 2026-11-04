---
layout: page
permalink: /cv/
title: cv
nav: false
nav_order: 5
description: My curriculum vitae
# The CV is deliberately not published on the site: no PDF is uploaded and this
# page is not built. Set `published: true` to turn it back on, and see
# _data/cv.yml if you ever want a rendered HTML CV instead of a PDF embed.
published: false
---

<div class="cv-container">
  <div class="pdf-viewer">
    <embed src="{{ '/assets/pdf/Wei_Chen_resume.pdf' | relative_url }}" type="application/pdf" width="100%" height="800px" style="border: 1px solid #ddd;" />
  </div>
</div>

<style>
.cv-container {
  max-width: 900px;
  margin: 0 auto;
  padding: 1rem;
}

.pdf-viewer {
  width: 100%;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  overflow: hidden;
}

.pdf-viewer embed {
  width: 100%;
  height: 800px;
  display: block;
}

@media (max-width: 768px) {
  .cv-container {
    padding: 0.5rem;
  }
  
  .pdf-viewer embed {
    height: 600px;
  }
}
</style>
