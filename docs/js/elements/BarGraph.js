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
  constructor(data, page_data, get_value, container_width, show_labels){
    const text_height = 20
    const width = container_width
    const height = container_width * 1.63
    this.height = height
    const margin = {top: 20, left: 20, right: 20, bottom: 20}
    // if(show_labels) margin.left = 140;

    const svgDom = document.createElementNS("http://www.w3.org/2000/svg", "svg")
    svgDom.setAttributeNS("http://www.w3.org/2000/xmlns/", "xmlns:xlink", "http://www.w3.org/1999/xlink");
    
    const avgs = this._compute_avg(data, get_value, d => d.page)
    const dataset = Object.keys(avgs).filter(k => k.indexOf('_') == -1)
      .map(p => ({ name: page_data[p].name, value: avgs[p]/page_data[p].likes }))

    this.svg = d3.select(svgDom)
      .attr('viewBox', '0,0,'+width+','+height)
      .attr('width', width)
      .attr('height', height)
      .attr('class', 'bargraph')
  
    const bar_x = d3.scaleLinear()
      .domain([0, d3.max(dataset, d => d.value)]).nice()
      .range([margin.left, width - margin.right])
  
    const bar_y = d3.scaleBand()
      .domain(dataset.map(d => d.name))
      .range([margin.top, height - margin.bottom])
      .padding(0.1)
    
    const bar_xAxis = g => g
      .attr("transform", `translate(0,${margin.top})`)
      .call(
        d3.axisTop(bar_x)
          .ticks(3)
      )
      .call(g => g.select(".domain").remove())
    
    const bar_yAxis = g => g
      .attr("transform", `translate(${margin.left},0)`)
      .call(
        d3.axisLeft(bar_y)
          .tickSize(0)
          .tickFormat("")
      )

    this.label_axis = g => g
      .attr("transform", `translate(${margin.left},0)`)
      .call(
        d3.axisLeft(bar_y)
          .tickSize(0)
      )
    
    this.svg.append("g")
        .attr("fill", "steelblue")
      .selectAll("rect").data(dataset).enter().append("rect")
        .attr("x", bar_x(0))
        .attr("y", d => bar_y(d.name))
        .attr("width", d => bar_x(d.value))
        .attr("height", bar_y.bandwidth());
    
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
      .attr('viewBox', '0,0,150'+this.height)

    labelSvg.append('g')
      .style('transform', 'translateX(150px)')
      .call(this.label_axis)

    return labelSvg
  }

  node(){
    return this.svg.node()
  }
}