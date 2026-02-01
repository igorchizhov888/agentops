#!/bin/bash

# Setup Google Analytics 4 for agentops GitHub Pages
# This script creates the necessary Jekyll configuration files

echo "Setting up Google Analytics 4 for agentops GitHub Pages..."
echo ""

# Your GA4 Measurement ID (same as other projects)
GA4_ID="G-DZJBQ7GZ4J"

# Create _config.yml
echo "Creating _config.yml..."
cat > _config.yml << 'EOF'
# GitHub Pages Jekyll Configuration
title: AgentOps
description: Enterprise Agent Operations Platform
theme: jekyll-theme-minimal

# Plugins
plugins:
  - jekyll-readme-index

# Use README.md as index
readme_index:
  enabled: true
EOF

echo "✓ Created _config.yml"

# Create _layouts directory
echo "Creating _layouts directory..."
mkdir -p _layouts

# Create default.html layout with GA4 tracking
echo "Creating _layouts/default.html with GA4 tracking..."
cat > _layouts/default.html << EOF
<!DOCTYPE html>
<html lang="en-US">
  <head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=${GA4_ID}"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      gtag('js', new Date());
      gtag('config', '${GA4_ID}');
    </script>

{% seo %}
    <link rel="stylesheet" href="{{ "/assets/css/style.css?v=" | append: site.github.build_revision | relative_url }}">
  </head>
  <body>
    <div class="wrapper">
      <header>
        <h1><a href="{{ "/" | absolute_url }}">{{ site.title | default: site.github.repository_name }}</a></h1>
        
        {% if site.logo %}
          <img src="{{site.logo | relative_url}}" alt="Logo" />
        {% endif %}

        <p>{{ site.description | default: site.github.project_tagline }}</p>

        {% if site.github.is_project_page %}
        <p class="view"><a href="{{ site.github.repository_url }}">View the Project on GitHub <small>{{ site.github.repository_nwo }}</small></a></p>
        {% endif %}

        {% if site.show_downloads %}
        <ul class="downloads">
          <li><a href="{{ site.github.zip_url }}">Download <strong>ZIP File</strong></a></li>
          <li><a href="{{ site.github.tar_url }}">Download <strong>TAR Ball</strong></a></li>
          <li><a href="{{ site.github.repository_url }}">View On <strong>GitHub</strong></a></li>
        </ul>
        {% endif %}
      </header>
      <section>

      {{ content }}

      </section>
      <footer>
        {% if site.github.is_project_page %}
        <p>This project is maintained by <a href="{{ site.github.owner_url }}">{{ site.github.owner_name }}</a></p>
        {% endif %}
        <p><small>Hosted on GitHub Pages &mdash; Theme by <a href="https://github.com/orderedlist">orderedlist</a></small></p>
      </footer>
    </div>
    <script src="{{ "/assets/js/scale.fix.js" | relative_url }}"></script>
  </body>
</html>
EOF

echo "✓ Created _layouts/default.html"
echo ""
echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
echo "Files created:"
echo "  1. _config.yml"
echo "  2. _layouts/default.html"
echo ""
echo "Next steps:"
echo "  1. Commit and push to GitHub:"
echo "     git add _config.yml _layouts/"
echo "     git commit -m 'Add Google Analytics 4 tracking'"
echo "     git push origin main"
echo ""
echo "  2. Wait 2-3 minutes for GitHub Pages to rebuild"
echo "  3. Visit https://igorchizhov888.github.io/agentops/"
echo "  4. Check Google Analytics (Real-Time report) to verify tracking"
echo ""
echo "Your GA4 Measurement ID: ${GA4_ID}"
echo "=========================================="
