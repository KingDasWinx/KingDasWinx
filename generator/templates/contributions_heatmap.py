"""SVG template: Neural Activity Contributions Heatmap (850x280)."""

from generator.utils import deterministic_random

WIDTH, HEIGHT = 850, 280


def _build_week_bars(weeks_data, max_contributions, theme):
    """Build animated contribution bars for each week."""
    bars = []
    bar_width = 8
    max_height = 120
    start_x = 60
    spacing = 12
    base_y = 200
    
    colors = [
        theme['synapse_cyan'],
        theme['dendrite_violet'],
        theme['axon_amber']
    ]
    
    for i, count in enumerate(weeks_data):
        if count == 0:
            continue
            
        x = start_x + (i * spacing)
        
        # Normalize height based on max contributions
        height = (count / max_contributions) * max_height if max_contributions > 0 else 10
        height = max(height, 4)  # Minimum height
        
        # Cycle through colors
        color = colors[i % len(colors)]
        
        # Animation delay based on position
        delay = f"{i * 0.02}s"
        
        # Glow filter
        bars.append(f'''    <defs>
      <filter id="bar-glow-{i}" x="-100%" y="-100%" width="300%" height="300%">
        <feGaussianBlur stdDeviation="2" result="blur"/>
        <feFlood flood-color="{color}" flood-opacity="0.6"/>
        <feComposite in2="blur" operator="in"/>
        <feMerge>
          <feMergeNode/>
          <feMergeNode in="SourceGraphic"/>
        </feMerge>
      </filter>
    </defs>''')
        
        # Bar with glow
        bars.append(f'''    <rect x="{x}" y="{base_y}" width="{bar_width}" height="0" 
          fill="{color}" opacity="0.8" rx="2" filter="url(#bar-glow-{i})">
      <animate attributeName="height" from="0" to="{height}" 
        dur="0.8s" begin="{delay}" fill="freeze"/>
      <animate attributeName="y" from="{base_y}" to="{base_y - height}" 
        dur="0.8s" begin="{delay}" fill="freeze"/>
      <animate attributeName="opacity" values="0.6;1;0.6" 
        dur="2s" begin="{delay}" repeatCount="indefinite"/>
    </rect>''')
        
        # Pulsing top dot
        bars.append(f'''    <circle cx="{x + bar_width/2}" cy="{base_y}" r="2" 
          fill="{color}" opacity="0">
      <animate attributeName="cy" from="{base_y}" to="{base_y - height}" 
        dur="0.8s" begin="{delay}" fill="freeze"/>
      <animate attributeName="opacity" values="0;1;0.7;1;0.7" 
        dur="2s" begin="{float(delay[:-1]) + 0.8}s" repeatCount="indefinite"/>
    </circle>''')
    
    return "\n".join(bars)


def _build_contribution_stats(total_contributions, streak, theme):
    """Build the stats display area."""
    stats = []
    
    # Total contributions display
    stats.append(f'''  <g class="stat-group">
    <text x="60" y="240" fill="{theme['text_faint']}" font-size="10" 
      font-family="monospace" letter-spacing="1">TOTAL CONTRIBUTIONS</text>
    <text x="60" y="265" fill="{theme['synapse_cyan']}" font-size="32" 
      font-weight="bold" font-family="sans-serif" opacity="0">
      {total_contributions}
      <animate attributeName="opacity" from="0" to="1" dur="0.6s" begin="0.5s" fill="freeze"/>
    </text>
  </g>''')
    
    # Current streak display
    stats.append(f'''  <g class="stat-group">
    <text x="280" y="240" fill="{theme['text_faint']}" font-size="10" 
      font-family="monospace" letter-spacing="1">CURRENT STREAK</text>
    <text x="280" y="265" fill="{theme['dendrite_violet']}" font-size="32" 
      font-weight="bold" font-family="sans-serif" opacity="0">
      {streak}
      <animate attributeName="opacity" from="0" to="1" dur="0.6s" begin="0.7s" fill="freeze"/>
    </text>
    <text x="330" y="265" fill="{theme['text_dim']}" font-size="16" 
      font-family="sans-serif" opacity="0">
      days
      <animate attributeName="opacity" from="0" to="0.6" dur="0.6s" begin="0.7s" fill="freeze"/>
    </text>
  </g>''')
    
    return "\n".join(stats)


def _build_neural_connections(theme):
    """Build animated neural connection lines in the background."""
    connections = []
    
    # Random connection points
    points_x = deterministic_random("neural-x", 8, 100, WIDTH - 100)
    points_y = deterministic_random("neural-y", 8, 60, 160)
    
    for i in range(len(points_x) - 1):
        x1, y1 = points_x[i], points_y[i]
        x2, y2 = points_x[i + 1], points_y[i + 1]
        
        color = theme['synapse_cyan'] if i % 2 == 0 else theme['dendrite_violet']
        delay = f"{i * 0.4}s"
        
        connections.append(f'''  <line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}"
    stroke="{color}" stroke-width="1" opacity="0" stroke-dasharray="5,5">
    <animate attributeName="opacity" values="0;0.15;0" dur="3s" 
      begin="{delay}" repeatCount="indefinite"/>
  </line>''')
        
        # Node points
        connections.append(f'''  <circle cx="{x1:.1f}" cy="{y1:.1f}" r="2" fill="{color}" opacity="0">
    <animate attributeName="opacity" values="0;0.4;0" dur="3s" 
      begin="{delay}" repeatCount="indefinite"/>
  </circle>''')
    
    return "\n".join(connections)


def _build_stars_background(theme):
    """Build subtle star particles in the background."""
    stars = []
    
    sx = deterministic_random("contrib-star-x", 20, 40, WIDTH - 40)
    sy = deterministic_random("contrib-star-y", 20, 40, HEIGHT - 40)
    sr = deterministic_random("contrib-star-r", 20, 0.5, 1.5)
    so = deterministic_random("contrib-star-o", 20, 0.05, 0.2)
    sd = deterministic_random("contrib-star-d", 20, 3.0, 6.0)
    
    colors = [theme['synapse_cyan'], theme['dendrite_violet'], theme['axon_amber'], theme['text_dim']]
    
    for i in range(20):
        color = colors[i % len(colors)]
        stars.append(f'''  <circle cx="{sx[i]:.1f}" cy="{sy[i]:.1f}" r="{sr[i]:.1f}" 
    fill="{color}" opacity="{so[i]:.2f}">
    <animate attributeName="opacity" 
      values="{so[i]:.2f};{min(so[i] * 2.5, 0.4):.2f};{so[i]:.2f}" 
      dur="{sd[i]:.1f}s" repeatCount="indefinite"/>
  </circle>''')
    
    return "\n".join(stars)


def _build_grid_overlay(theme):
    """Build subtle grid lines."""
    lines = []
    
    # Horizontal lines
    for y in range(60, HEIGHT - 20, 40):
        lines.append(f'''  <line x1="30" y1="{y}" x2="{WIDTH - 30}" y2="{y}"
    stroke="{theme['text_faint']}" stroke-width="0.5" 
    stroke-dasharray="4,8" opacity="0.08"/>''')
    
    # Vertical lines
    for x in range(100, WIDTH - 50, 100):
        lines.append(f'''  <line x1="{x}" y1="50" x2="{x}" y2="210"
    stroke="{theme['text_faint']}" stroke-width="0.5" 
    stroke-dasharray="4,8" opacity="0.06"/>''')
    
    return "\n".join(lines)


def _build_scanning_effect(theme):
    """Build a scanning line effect across the card."""
    return f'''  <rect x="30" y="50" width="2" height="160" 
    fill="{theme['synapse_cyan']}" opacity="0.15">
    <animate attributeName="x" from="30" to="{WIDTH - 30}" 
      dur="4s" repeatCount="indefinite"/>
  </rect>'''


def render(contributions_data: dict, theme: dict) -> str:
    """Render the contributions heatmap SVG.
    
    Args:
        contributions_data: dict with keys:
            - weeks: list of contribution counts per week (last 52 weeks)
            - total: total contributions in the period
            - streak: current contribution streak in days
        theme: color palette dict
    """
    weeks = contributions_data.get('weeks', [])
    total = contributions_data.get('total', 0)
    streak = contributions_data.get('streak', 0)
    
    # Limit to last 52 weeks and pad if needed
    weeks = weeks[-52:] if len(weeks) > 52 else weeks
    if len(weeks) < 52:
        weeks = [0] * (52 - len(weeks)) + weeks
    
    max_contributions = max(weeks) if weeks else 1
    
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}">
  <defs>
    <style>
      @keyframes pulse-glow {{
        0%, 100% {{ opacity: 0.6; }}
        50% {{ opacity: 1; }}
      }}
      .stat-group text {{
        animation: pulse-glow 3s ease-in-out infinite;
      }}
    </style>
  </defs>

  <!-- Background -->
  <rect x="0.5" y="0.5" width="{WIDTH - 1}" height="{HEIGHT - 1}" rx="12" ry="12"
    fill="{theme['nebula']}" stroke="{theme['star_dust']}" stroke-width="1"/>

  <!-- Background stars -->
{_build_stars_background(theme)}

  <!-- Grid overlay -->
{_build_grid_overlay(theme)}

  <!-- Neural connections -->
{_build_neural_connections(theme)}

  <!-- Title -->
  <text x="30" y="38" fill="{theme['text_faint']}" font-size="11" 
    font-family="monospace" letter-spacing="3">NEURAL ACTIVITY PATTERN</text>
  
  <!-- Status indicator -->
  <circle cx="235" cy="34" r="3" fill="{theme['axon_amber']}">
    <animate attributeName="opacity" values="0.4;1;0.4" dur="2s" repeatCount="indefinite"/>
  </circle>

  <!-- Time range label -->
  <text x="{WIDTH - 30}" y="38" fill="{theme['text_faint']}" font-size="10" 
    font-family="monospace" text-anchor="end" opacity="0.5">LAST 52 WEEKS</text>

  <!-- Contribution bars -->
{_build_week_bars(weeks, max_contributions, theme)}

  <!-- Stats display -->
{_build_contribution_stats(total, streak, theme)}

  <!-- Scanning effect -->
{_build_scanning_effect(theme)}

  <!-- Baseline -->
  <line x1="60" y1="200" x2="{WIDTH - 60}" y2="200" 
    stroke="{theme['star_dust']}" stroke-width="1.5" opacity="0.4"/>
</svg>'''
