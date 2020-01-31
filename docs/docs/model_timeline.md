---
layout: primer
title: Model Timeline
nav_order: 4
---
<div>
{% for event in site.data.model_events %}
    <div class="TimelineItem">
        <div class="TimelineItem-badge">
        {% octicon {{ event.icon }} %}
        </div>
        <div class="TimelineItem-body">
        <span>{{ event.event_type }}, {{ event.comment }}<br><p class="f6">{{ event.datetime }}</p></span>
        </div>
        <div class="d-flex flex-column">
          <p class="branch-name">
            {% octicon git-commit %} <a href="{{ event.reference }}">{{ event.link }}</a>
          </p>
          <div></div>
        </div>
    </div>
{% endfor %}
</div>