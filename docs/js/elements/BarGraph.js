class BarGraph{
  _compute_avg(dataset, getter, group_by){
    return dataset.reduce((avgs, d) => {
      const k = group_by(d)
      if(!avgs[k+'_sum'])
        avgs[k+'_sum'] = 0.0
      avgs[k+'_sum'] += getter(d)

      if(!avgs[k+'_count'])
        avgs[k+'_count'] = 0.0
      avgs[k+'_count'] += 1.0

      avgs[k] = avgs[k+'_sum'] / avgs[k+'_count']
      return avgs
    }, {})
  }
  constructor(page_data, get_value, container_width, show_labels){
    const text_height = 20
    this.width = container_width
    this.height = container_width * 1.63
    this.margin = {top: 20, left: 20, right: 20, bottom: 20}
    this.get_value = get_value
    this.page_data = page_data
    // if(show_labels) margin.left = 140;

    const svgDom = document.createElementNS("http://www.w3.org/2000/svg", "svg")
    svgDom.setAttributeNS("http://www.w3.org/2000/xmlns/", "xmlns:xlink", "http://www.w3.org/1999/xlink");
    
    this.svg = d3.select(svgDom)
      .attr('viewBox', '0,0,'+this.width+','+this.height)
      .attr('width', this.width)
      .attr('height', this.height)
      .attr('class', 'bargraph')

    this.bar_group = this.svg.append("g")
      .attr("fill", "steelblue")
  }

  update(data){
    const avgs = this._compute_avg(data, this.get_value, d => d.page)
    const dataset = Object.keys(avgs).filter(k => k.indexOf('_') == -1)
      .map(p => ({ name: this.page_data[p].name, value: avgs[p]/this.page_data[p].likes }))

    const bar_x = d3.scaleLinear()
      .domain([0, d3.max(dataset, d => d.value)]).nice()
      .range([this.margin.left, this.width - this.margin.right])
  
    const bar_y = d3.scaleBand()
      .domain(dataset.map(d => d.name))
      .range([this.margin.top, this.height - this.margin.bottom])
      .padding(0.1)
    
    const bar_xAxis = g => g
      .attr("transform", `translate(0,${this.margin.top})`)
      .call(
        d3.axisTop(bar_x)
          .ticks(3)
      )
      .call(g => g.select(".domain").remove())
    
    const bar_yAxis = g => g
      .attr("transform", `translate(${this.margin.left},0)`)
      .call(
        d3.axisLeft(bar_y)
          .tickSize(0)
          .tickFormat("")
      )

    this.label_axis = g => g
      .attr("transform", `translate(${this.margin.left},0)`)
      .call(
        d3.axisLeft(bar_y)
          .tickSize(0)
      )
    
    
    const bars = this.bar_group.selectAll("rect")
      .data(dataset, d => d.name)

    bars.enter().append("rect")
      .attr("x", bar_x(0))
      .attr("y", d => bar_y(d.name))
      .attr("width", d => bar_x(d.value))
      .attr("height", bar_y.bandwidth())
      .style('opacity', 0)
      .transition()
        .style('opacity', 1)

    bars
      .transition()
        .attr('width', d => bar_x(d.value))

    bars.exit()
      .transition()
        .style('opacity', 0)
        .remove()
    
    // this.svg.append("g")
    //   .call(bar_xAxis);
    
    this.svg.append("g")
      .call(bar_yAxis);
  }

  labels(){
    const svgDom = document.createElementNS("http://www.w3.org/2000/svg", "svg")
    svgDom.setAttributeNS("http://www.w3.org/2000/xmlns/", "xmlns:xlink", "http://www.w3.org/1999/xlink");
    const labelSvg = d3.select(svgDom)
      .attr('width', 150)
      .attr('height', this.height)
      .attr('viewBox', '0,0,150,'+this.height)

    labelSvg.append('g')
      .style('transform', 'translateX(150px)')
      .call(this.label_axis)

    return labelSvg
  }

  node(){
    return this.svg.node()
  }
}