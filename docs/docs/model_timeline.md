---
layout: default
title: Model Timeline
nav_order: 4
---

<center><p class="label label-red" style="opacity: 0.6;">Mockup / Illustrative</p></center>

<link href="https://unpkg.com/@primer/css/dist/primer.css" rel="stylesheet" />
<style>
  a.navigation-list-link {color: #7253ed}
</style>

<ul>
{% for event in site.data.model_events %}
  <li>
    <div class="TimelineItem">
        <div class="TimelineItem-badge">
        {% octicon { event.icon } %}
        </div>
        <div class="TimelineItem-body">
    
        <span>{ event.event_type}, { event.comment}</span>
        <br>
        </div>
        <p class="branch-name">
            {% octicon git-commit %} <a href="{ event.reference }">{ event.link }</a>
        </p>
    </div>
  </li>
{% endfor %}
</ul>