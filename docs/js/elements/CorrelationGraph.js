function CorrelationGraph(width, height, graph_margin) {
  const CORRELATION_REACTIONS = REACTIONS.filter(r => r != 'share' && r != 'comment' && r != 'like')
  const max_react = d => {
    const reax_values = CORRELATION_REACTIONS.map(r => d[r+"_count"])
    const i = d3.scan(reax_values, function(a, b) { return b - a; });
    return CORRELATION_REACTIONS[i]
  }
  
  // Add 1 to values so we don't have Infinite datasets
  const get_x = d => d.total_count + 1
  const get_y = d => d.share_count + 1

  const margin = graph_margin || {left: 25, right: 25, top: 25, bottom: 25}

  const svgDom = document.createElementNS("http://www.w3.org/2000/svg", "svg")
  svgDom.setAttributeNS("http://www.w3.org/2000/xmlns/", "xmlns:xlink", "http://www.w3.org/1999/xlink");
  const svg = d3.select(svgDom)
      .attr('width', width)
      .attr('height', height)
  
  var x = false, y = false

  const correlation_box = svg.append("g")
    .attr('class', 'correlations')

  correlation_box.append('text')
    .attr('x', margin.left+80)
    .attr('y', margin.top)
    .attr('width', 50)
    .attr('height', 15)
    .attr('text-anchor', 'top')
    .attr('font-weight', 'bold')
    .text('R2 Values')


  const dot_group = svg.append('g')
    .attr('class', 'scatterplot')

  function update(data, reaction_filter){
    const dataset = data
      .filter(d => get_x(d) > 0 && get_y(d) > 0)

    if(!x || !y){

      x = d3.scaleLog()
        .domain(d3.extent(dataset, get_x)).nice()
        .range([margin.left, width - margin.right])

      y = d3.scaleLog()
        .domain(d3.extent(dataset, get_y)).nice()
        .range([height - margin.bottom, margin.top])
      const xAxis = g => g
        .attr("transform", `translate(0,${height - margin.bottom})`)
        .call(d3.axisBottom(x))
        .call(g => g.select(".domain").remove())
        .call(g => g.append("text")
          .attr("x", width - margin.right)
          .attr("y", -4)
          .attr("fill", "#000")
          .attr("font-weight", "bold")
          .attr("text-anchor", "end")
          .text("Combined Reactions"))
      
      const yAxis = g => g
        .attr("transform", `translate(${margin.left},0)`)
        .call(d3.axisLeft(y))
        .call(g => g.select(".domain").remove())
        .call(g => g.append("text")
          .attr("fill", "#000")
          .attr("x", 5)
          .attr("y", margin.top)
          .attr("dy", "0.32em")
          .attr("text-anchor", "start")
          .attr("font-weight", "bold")
          .text("Shares"))

      svg.append("g").attr('class', 'axis')
        .call(xAxis);
      
      svg.append("g").attr('class', 'axis')
        .call(yAxis);
    }
    
    const reactions_grouped = CORRELATION_REACTIONS.filter(reax => (!reaction_filter || reax == reaction_filter))
      .map(reax => {
        return data.filter(d => max_react(d) == reax)//.filter(d => x(get_x(d)) && y(get_y(d)))
      }).filter(reax_data => reax_data.length > 0);
    
    const reaction_lines = reactions_grouped.map(reax_data => {
        const reg = regressionjs.linear(reax_data.map(d => [x(get_x(d)), y(get_y(d))]))
        return {
          reaction: max_react(reax_data[0]),
          reg: reg,
          line_p1: reg.points[d3.scan(reg.points, (a,b) => a[0] - b[0])],
          line_p2: reg.points[d3.scan(reg.points, (a,b) => b[0] - a[0])]
        }
      })

    const correlation_group = svg.selectAll('.correlation-group')
      .data( reaction_lines, d => d.reaction )
      
    const new_group = correlation_group.enter()
      .append('g')
      .attr('class', 'correlation-group')
      .style('opacity', 0)

    new_group.append('line')
      .attr("x1", d => d.line_p1[0])
      .attr("y1", d => d.line_p1[1])
      .attr("x2", d => d.line_p2[0])
      .attr("y2", d => d.line_p2[1])
      .attr("stroke", d => REACTION_COLORS[d.reaction])
      .attr("stroke-width", 2)

    new_group.append("image")
      .attr('x', d => d.line_p2[0])
      .attr('y', d => d.line_p2[1])
      .attr('width', 20)
      .attr('height', 20)
      .attr('transform', 'translate(1,-17)')
      .attr("xlink:href",d=>"https://peterandringa.com/facebook-news-analysis/img/reactions/"+d.reaction+".png")

    new_group
      .transition()
        .style('opacity', 1)

    // Updating lines
    correlation_group.select('line')
      .transition()
        .attr("x1", d => d.line_p1[0])
        .attr("y1", d => d.line_p1[1])
        .attr("x2", d => d.line_p2[0])
        .attr("y2", d => d.line_p2[1])

    correlation_group.select('image')
      .transition()
        .attr('x', d => d.line_p2[0])
        .attr('y', d => d.line_p2[1])

    correlation_group.exit()
      .transition()
        .style("opacity", 0)
        .remove()

    const info_group = correlation_box.selectAll('g')
      .data( reaction_lines, d => d.reaction )

    info_group.select('text')
      .transition()
        .attr('y', (d,i) => i*20 + margin.top + 18)
        .text(d => d.reg.r2)

    info_group.select('image')
      .transition()
        .attr('y', (d,i) => i*20 + margin.top + 6)

    info_group.exit()
      .transition()
        .style('opacity', 0)
        .remove()

    const new_info = info_group.enter()
      .append('g')
      .style('opacity', 0)

    new_info
      .append("image")
      .attr('x', 80 + margin.left)
      .attr('y', (d,i) => i*20 + margin.top + 6)
      .attr('width', 12)
      .attr('height', 12)
      .attr("xlink:href",d => "https://peterandringa.com/facebook-news-analysis/img/reactions/"+d.reaction+".png")

    new_info
      .append("text")
      .attr('x', 95 + margin.left)
      .attr('y', (d,i) => i*20 + margin.top + 18)
      .attr('width', 50)
      .attr('height', 15)
      .attr('font-weight', 'normal')
      .text(d => d.reg.r2)

    new_info
      .transition()
        .style('opacity', 1)

    const dot_data = reaction_filter ? reactions_grouped[0] : [];
    
    const dots = dot_group.selectAll('circle')
      .data( dot_data, d => d.fb_id )

    // Create
    dots.enter()
      .append("circle")
      .attr("transform", d => `translate(${x(get_x(d))},${y(get_y(d))})`)
      .attr("r", 2)
      .attr('fill', REACTION_COLORS[reaction_filter])
      .attr('opacity', 0)
      .transition()
        .attr('opacity', 0.5)

    // Destroy
    dots.exit()
      .transition()
        .attr('opacity', 0)
        .remove()

    // Update
    dots
      .transition()
        .attr("transform", d => `translate(${x(get_x(d))},${y(get_y(d))})`)
  }

  return {
    svg: svg.node(),
    update: update,
    reactions: CORRELATION_REACTIONS
  }
}
