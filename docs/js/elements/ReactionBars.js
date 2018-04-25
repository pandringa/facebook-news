class ReactionBars {
  constructor(title, container_width){
    this.height = 100
    this.text_width = 84
    this.width = (container_width / 4.0) - 20
    this.title = title

    const svgDom = document.createElementNS("http://www.w3.org/2000/svg", "svg")
    svgDom.setAttributeNS("http://www.w3.org/2000/xmlns/", "xmlns:xlink", "http://www.w3.org/1999/xlink");
    
    this.svg = d3.select(svgDom)
      .attr('viewBox', '0,0,'+this.width+','+this.height)
      .attr('width', this.width)
      .attr('height', this.height)
      .attr('class', 'barset barset-'  + title.replace(' ', '-'))

    // Set up label
    const label = this.svg.append('text')
      .text(d => this.title)
      .attr('y', this.height / 2 + 5)
      .attr('x', this.text_width - 22)
      .attr('text-anchor', 'end')
      .attr('font-size', 13)
     
    this.bar_group = this.svg.append("g")
  }

  _transformData(dataset){
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

  update(dataset){
    const data = this._transformData(dataset)
    console.log(data)
    const bar_x = d3.scaleLinear()
      .domain([0, d3.max(data, d => d.count)]).nice()
      .range([0, this.width - this.text_width])

    const bar_y = d3.scaleBand()
      .domain(data.map(d => d.name))
      .range([0, this.height])
      .padding(0.2)

    const emoji = this.svg.append("g")
      .selectAll('image').data(data)
        .enter().append('image')
          .attr('x', this.text_width - this.height/8 - 4)
          .attr('y', d => bar_y(d.name) + 2)
          .attr('width', this.height/8)
          .attr('height', this.height/8)
          .attr("xlink:href", d => "https://peterandringa.com/facebook-news/img/reactions/"+d.name+".png")
    
    const bars = this.bar_group.selectAll('rect')
      .data(data, d => d.name)

    bars.enter()
      .append("rect")
        .attr("fill", d => REACTION_COLORS[d.name])
        .attr("x", bar_x(0) + this.text_width)
        .attr("y", d => bar_y(d.name))
        .attr("height", bar_y.bandwidth())
        .attr("width", d => bar_x(d.count))

    bars
      .attr('class', 'updated')
      .transition()
        .attr("width", d => bar_x(d.count))
  }

  node() {
    return this.svg.node()
  }

  title() {
    return this.title
  }
}