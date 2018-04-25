function ReactionBars(title, container_width){
  const height = 100
  const text_width = 84
  const width = (container_width / 4.0) - 20
  const svgDom = document.createElementNS("http://www.w3.org/2000/svg", "svg")
  svgDom.setAttributeNS("http://www.w3.org/2000/xmlns/", "xmlns:xlink", "http://www.w3.org/1999/xlink");
  const svg = d3.select(svgDom)
    .attr('viewBox', '0,0,'+width+','+height)
    .attr('width', width)
    .attr('height', height)
    .attr('class', 'barset barset-'  + title.replace(' ', '-'))

  // Set up label
  const label = svg.append('text')
    .text(d => title)
    .attr('y', height / 2 + 5)
    .attr('x', text_width - 22)
    .attr('text-anchor', 'end')
    .attr('font-size', 13)
   
  const bar_group = svg.append("g")

  function transformData(dataset){
    const reactions = REACTIONS.filter(r => ['like','share','comment'].indexOf(r) == -1)
    const reax_data = {}
    for(var post of dataset){
      for(var reax of reactions){
        if(!reax_data[reax]) reax_data[reax] = 0
        reax_data[reax] += post[reax+"_count"];
      }
    }
    return Object.keys(reax_data).map(r => ({count:reax_data[r], name:r}) )
  }

  function update(dataset){
    const data = transformData(dataset)

    const bar_x = d3.scaleLinear()
      .domain([0, d3.max(data, d => d.count)]).nice()
      .range([0, width - text_width])

    const bar_y = d3.scaleBand()
      .domain(data.map(d => d.name))
      .range([0, height])
      .padding(0.2)

    const emoji = svg.append("g")
      .selectAll('image').data(data)
        .enter().append('image')
          .attr('x', text_width - height/8 - 4)
          .attr('y', d => bar_y(d.name) + 2)
          .attr('width', height/8)
          .attr('height', height/8)
          .attr("xlink:href", d => "https://peterandringa.com/facebook-news-analysis/img/reactions/"+d.name+".png")
    
    const bars = bar_group.selectAll('rect')
      .data(data, d => d.name)

    bars.enter()
      .append("rect")
        .attr("fill", d => REACTION_COLORS[d.name])
        .attr("x", bar_x(0) + text_width)
        .attr("y", d => bar_y(d.name))
        .attr("height", bar_y.bandwidth())
        .attr("width", d => bar_x(d.count))

    bars
      .attr('class', 'updated')
      .transition()
        .attr("width", d => bar_x(d.count))
  }

  return {
    svg: svg,
    update: update,
    title: title
  }
}