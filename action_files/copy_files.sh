#!/bin/bash

set -e
# set -ex

echo "---
layout: primer
title: Summary
permalink: /summary
nav_order: 2
---

1. TOC
{:toc}" > project/temp.md && for f in project/temp.md project/model_card.md; do cat "$f"; echo " "; done > project/output.md && mv project/output.md docs/docs/model_card.md
echo "---
layout: primer
title: Data Dictionary
nav_order: 3
---

1. TOC
{:toc}" > project/temp.md && for f in project/temp.md project/data_dictionary.md; do cat "$f"; echo " "; done > project/output.md && mv project/output.md docs/docs/data_dictionary.md     
cp project/model_events.csv docs/_data/model_events.csv