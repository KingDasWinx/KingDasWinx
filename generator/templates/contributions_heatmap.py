"""SVG template: Neural Activity Contributions Heatmap (850x280)."""

from generator.utils import deterministic_random

WIDTH, HEIGHT = 850, 300


def _build_day_bars(days_data, max_contributions, theme):
    """Build animated contribution bars for each day."""
    bars = []
    bar_width = 2
    max_height = 120
    start_x = 60
    available_width = WIDTH - (start_x * 2)  # 730px
    spacing = available_width / max(len(days_data), 1)
    base_y = 200
    
    colors = [
        theme['synapse_cyan'],
        theme['dendrite_violet'],
        theme['axon_amber']
    ]
    
    # Create shared filter defs at the start
    filters = []
    for idx, color in enumerate(colors):
        filters.append(f'''    <filter id="bar-glow-{idx}" x="-100%" y="-100%" width="300%" height="300%">
      <feGaussianBlur stdDeviation="1.5" result="blur"/>
      <feFlood flood-color="{color}" flood-opacity="0.5"/>
      <feComposite in2="blur" operator="in"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>''')
    
    bars.extend(filters)
    
    for i, count in enumerate(days_data):
        if count == 0:
            continue
            
        x = start_x + (i * spacing)
        
        # Normalize height based on max contributions
        height = (count / max_contributions) * max_height if max_contributions > 0 else 10
        height = max(height, 3)  # Minimum height
        
        # Cycle through colors (change every ~30 days for monthly variance)
        color_idx = (i // 30) % len(colors)
        color = colors[color_idx]
        
        # Animation delay based on position (faster for many elements)
        delay = f"{i * 0.005}s"
        
        # Bar with glow
        bars.append(f'''    <rect x="{x:.1f}" y="{base_y}" width="{bar_width}" height="0" 
          fill="{color}" opacity="0.8" rx="1" filter="url(#bar-glow-{color_idx})">
      <animate attributeName="height" from="0" to="{height:.1f}" 
        dur="0.6s" begin="{delay}" fill="freeze"/>
      <animate attributeName="y" from="{base_y}" to="{base_y - height:.1f}" 
        dur="0.6s" begin="{delay}" fill="freeze"/>
      <animate attributeName="opacity" values="0.6;1;0.6" 
        dur="2s" begin="{delay}" repeatCount="indefinite"/>
    </rect>''')
    
    return "\n".join(bars)


def _build_contribution_stats(total_contributions, streak, theme):
    """Build the stats display area."""
    stats = []
    
    # Total contributions display
    stats.append(f'''  <g class="stat-group">
    <text x="60" y="240" fill="{theme['text_faint']}" font-size="10" 
      font-family="monospace" letter-spacing="1" text-anchor="start">TOTAL CONTRIBUTIONS</text>
    <text x="60" y="275" fill="{theme['synapse_cyan']}" font-size="32" 
      font-weight="bold" font-family="sans-serif" text-anchor="start" opacity="0">
      {total_contributions}
      <animate attributeName="opacity" from="0" to="1" dur="0.6s" begin="0.5s" fill="freeze"/>
    </text>
  </g>''')
    
    # Current streak display
    streak_text_width = len(str(streak)) * 20
    days_x = 300 + streak_text_width
    
    stats.append(f'''  <g class="stat-group">
    <text x="300" y="240" fill="{theme['text_faint']}" font-size="10" 
      font-family="monospace" letter-spacing="1" text-anchor="start">CURRENT STREAK</text>
    <text x="300" y="275" fill="{theme['dendrite_violet']}" font-size="32" 
      font-weight="bold" font-family="sans-serif" text-anchor="start" opacity="0">
      {streak}
      <animate attributeName="opacity" from="0" to="1" dur="0.6s" begin="0.7s" fill="freeze"/>
    </text>
    <text x="{days_x}" y="275" fill="{theme['text_dim']}" font-size="16" 
      font-family="sans-serif" text-anchor="start" dominant-baseline="alphabetic" opacity="0">
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
            - days: list of contribution counts per day (current year)
            - total: total contributions in current year
            - streak: current contribution streak in days
        theme: color palette dict
    """
    days = contributions_data.get('days', [])
    total = contributions_data.get('total', 0)
    streak = contributions_data.get('streak', 0)
    
    # Ensure we have data
    if not days:
        days = [0]
    
    max_contributions = max(days) if days else 1
    
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
  <text x="30" y="40" fill="{theme['text_faint']}" font-size="11" 
    font-family="monospace" letter-spacing="3">NEURAL ACTIVITY</text>
  
  <!-- Status indicator -->
  <circle cx="235" cy="34" r="3" fill="{theme['axon_amber']}">
    <animate attributeName="opacity" values="0.4;1;0.4" dur="2s" repeatCount="indefinite"/>
  </circle>

  <!-- Time range label -->
  <text x="{WIDTH - 30}" y="38" fill="{theme['text_faint']}" font-size="10" 
    font-family="monospace" text-anchor="end" opacity="0.5">CURRENT YEAR</text>

  <!-- Contribution bars -->
{_build_day_bars(days, max_contributions, theme)}

  <!-- Stats display -->
{_build_contribution_stats(total, streak, theme)}

  <!-- Scanning effect -->
{_build_scanning_effect(theme)}

  <!-- Baseline -->
  <line x1="60" y1="200" x2="{WIDTH - 60}" y2="200" 
    stroke="{theme['star_dust']}" stroke-width="1.5" opacity="0.4"/>
</svg>'''
