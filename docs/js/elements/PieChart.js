class PieChart {
  constructor(title, container_width){
    const text_height = 20
    const width = container_width
    const radius = container_width / 2 - 10
    const height = container_width + text_height
    const svgDom = document.createElementNS("http://www.w3.org/2000/svg", "svg")
    svgDom.setAttributeNS("http://www.w3.org/2000/xmlns/", "xmlns:xlink", "http://www.w3.org/1999/xlink");
    
    this.svg = d3.select(svgDom)
      .attr('viewBox', '0,0,'+width+','+height)
      .attr('width', width)
      .attr('height', height)
      .attr('class', 'pie pie-'+title.replace(' ', '-'))

    // Set up label
    const label = this.svg.append('text')
      .text(d => title)
      .attr('y', 20)
      .attr('x', width / 2)
      .attr('text-anchor', 'middle')
      .attr('font-size', 11)


    this.pie = d3.pie()
        .sort(null)
        .value(d => d.value);

    this.path = d3.arc()
      .outerRadius(radius - 10)
      .innerRadius(0);
     
    this.pie_group = this.svg.append("g")
      .attr('transform', 'translate('+width/2+','+height/2+')')
  }

  update(dataset){
    const max = dataset.reduce( (max, d) => {
      if(d.value > max[0])
        return [d.value, d.name]
      else
        return max
    }, [0,''])
    
    const slices = this.pie_group.selectAll(".arc")
      .data(this.pie(dataset))
      .enter().append("g")
        .attr("class", "arc")
        .append("path")
        .attr("fill", d => d.data.color)
        .attr('opacity', d => (d.data.name == max[1]) ? 1 : 0.1)
        .attr("d", this.path)      
  }

  node() {
    return this.svg.node()
  }
}