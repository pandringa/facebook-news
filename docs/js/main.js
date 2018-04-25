/*******************
*  CONSTANTS
********************/
const CATEGORIES = ['national','politics','business','science','world','sports','lifestyle','opinion']
const CATEGORY_COLORS = {
  national: '#80b1d3',
  politics: '#fb8072',
  business: '#8dd3c7',
  science: '#EEEE93',
  world: '#bebada',
  sports: '#fdb462',
  lifestyle: '#b3de69',
  opinion: '#fccde5'
}
const PAGES = {
  'cnn': 'CNN',
  'foxnews': 'Fox News',
  'nytimes': 'The New York Times',
  'abcnews': 'ABC News',
  'huffpost': 'HuffPost',
  'nbcnews': 'NBC News',
  'usatoday': 'USA TODAY',
  'npr': 'NPR',
  'wsj': 'The Wall Street Journal',
  'washingtonpost': 'Washington Post',
  'cbsnews': 'CBS News',
  'reuters': 'Reuters',
  'breitbart': 'Breitbart',
  'latimes': 'Los Angeles Times',
}
const REACTIONS = ['like', 'love', 'haha', 'wow', 'sad', 'angry', 'comment', 'share']
const REACTION_COLORS = {
  'like': '#5C89E5',
  'love': '#FB8072',
  'haha': '#8FDDD0',
  'wow': '#EEEE93',
  'sad': '#B1AAE1',
  'angry': '#FDB462',
  'comment': '#72D582',
  'share': '#4C4BA6',
}


/*******************
*  REACTION BARS
********************/

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

/*******************
*  PIE CHARTS
********************/
function PieChart(title, container_width){
  const text_height = 20
  const width = container_width
  const radius = container_width / 2 - 10
  const height = container_width + text_height
  const svgDom = document.createElementNS("http://www.w3.org/2000/svg", "svg")
  svgDom.setAttributeNS("http://www.w3.org/2000/xmlns/", "xmlns:xlink", "http://www.w3.org/1999/xlink");
  const svg = d3.select(svgDom)
    .attr('viewBox', '0,0,'+width+','+height)
    .attr('width', width)
    .attr('height', height)
    .attr('class', 'pie pie-'+title.replace(' ', '-'))

  // Set up label
  const label = svg.append('text')
    .text(d => title)
    .attr('y', 20)
    .attr('x', width / 2)
    .attr('text-anchor', 'middle')
    .attr('font-size', 11)


  const pie = d3.pie()
      .sort(null)
      .value(d => d.value);

  const path = d3.arc()
    .outerRadius(radius - 10)
    .innerRadius(0);
   
  const pie_group = svg.append("g")
    .attr('transform', 'translate('+width/2+','+height/2+')')

  function update(dataset){
    const max = dataset.reduce( (max, d) => {
      if(d.value > max[0])
        return [d.value, d.name]
      else
        return max
    }, [0,''])
    
    const slices = pie_group.selectAll(".arc")
      .data(pie(dataset))
      .enter().append("g")
        .attr("class", "arc")
        .append("path")
        .attr("fill", d => d.data.color)
        .attr('opacity', d => (d.data.name == max[1]) ? 1 : 0.1)
        .attr("d", path)      
  }

  return {
    svg: svg,
    update: update
  }
}

function Table(dataset, headers){
  const container = d3.select(document.createElement('table'))
  const header_el = container.append('tr').classed('header', true)
  header_el.append('th').classed('empty', true).text(' ')
  header_el.selectAll('th:not(.empty)').data(headers)
    .enter().append('th')
      .append('img')
        .attr("src", d => "https://peterandringa.com/facebook-news-analysis/img/reactions/"+d+".png")


  for(var row of Object.keys(dataset)){
    const row_el = container.append('tr')
    row_el.append('th')
      .text(PAGES[row])

    row_el.selectAll('td').data(headers)
    .enter().append('td')
      .text(h => dataset[row][h].category)
      .style('background', h => CATEGORY_COLORS[dataset[row][h].category])
  }

  return container
}

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

    console.log('filter', reaction_filter)
    console.log('groups', reactions_grouped)
    const dot_data = reaction_filter ? reactions_grouped[0] : [];
    console.log('data', dot_data)
    
    const dots = dot_group.selectAll('circle')
      .data( dot_data, d => d.fb_id )

    console.log('dots', dots)

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



function Select(choices, placeholder, width){
  // Image
  const itemTemplate = options => `
    <div 
      class="
        selectivity-result-item 
        ${options.disabled ? 'disabled' : ''}
      "
      data-item-id="${options.id}"
    >
      ${options.text}
      ${options.submenu
          ? '<i class="selectivity-submenu-icon fa fa-chevron-right"></i>'
          : ''}
    </div>`;
  const selectedTemplate = options => `
    <span 
      class="
        selectivity-single-selected-item
      "
      data-item-id="${options.id}"
    >
      ${options.removable
          ? '<a class="selectivity-single-selected-item-remove">' +
            '<i class="fa fa-remove"></i>' +
            '</a>'
          : ''}
      ${options.text}
    </span>`

  var element = document.createElement('div')
  element.setAttribute('class', 'dropdown')
  element.setAttribute('style', 'width: '+width+'px')

  if(typeof choices == 'object'){
    choices = Object.keys(choices).map(k => ({
      id: k, text: choices[k]
    })).sort( (a,b) => d3.ascending(a.text, b.text) )
  }else{
    choices = choices.sort( (a,b) => d3.ascending(a, b) )
  }

  var singleInput = new Selectivity.Inputs.Single({
    element: element,
    items: choices,
    allowClear: true,
    placeholder: placeholder,
    templates: {
      resultItem: itemTemplate,
      singleSelectedItem: selectedTemplate
    },
  });

  return element
}

function buildReactionBars(data){
  const container = d3.select('#bars-container');
  const containerWidth = +container.style('width').slice(0, -2)
  const category_bars = []
  
  for(var c of CATEGORIES ){
    const bars = ReactionBars(c, containerWidth)
    bars.update( data.filter(d => d.category == c) )
    container.node().appendChild(bars.svg.node())
    category_bars.push( bars )
  }

  const page_select = Select( PAGES, 'All News Sources', 250 )
  
  page_select.addEventListener('change', e => {
    category_bars.forEach(b => {
      const newData = data.filter(d => d.title == b.category && (!e.value || d.page == e.value) )
      b.update( newData )
    })
  });

  d3.select('#reaction-selects').node()
    .appendChild( page_select )

  return data
}

function buildCategoryPies(data){
  const container = d3.select('#pies-container')
  const containerWidth = +container.style('width').slice(0, -2)
  
  for(var p of Object.keys(PAGES).sort( (a,b) => d3.ascending(a, b) ) ){
    var pie_data = data.filter(d => d.page == p)
    .reduce( (obj, d) => {
      if(!obj[d.category]) obj[d.category] = 0
      obj[d.category]++;
      return obj
    }, {})

    pie_data = Object.keys(pie_data).map(c => ({
      name: c,
      value: pie_data[c],
      color: CATEGORY_COLORS[c]
    })).sort((a,b) => d3.descending(a.name, b.name))
    const pie = PieChart(PAGES[p], containerWidth/7)
    pie.update( pie_data )
    container.node().appendChild(pie.svg.node())
  }

  const legends = d3.select('#pies-legend')
    .selectAll('.legend-item')
    .data( Object.keys(CATEGORY_COLORS).map(c => ({name: c, color: CATEGORY_COLORS[c]}) ) )
    .enter()
      .append('div')
        .classed('legend-item', true)
        .style('color', d => d.color)
        .text(d => d.name)
        .append('span')
          .classed('legend-color', true)
          .style('background', d => d.color)

  return data
}

function buildCategoryTable(data){
  const container = d3.select('#table-container')
  const table_rows = {}
  for(var p of Object.keys(PAGES).sort( (a,b) => d3.ascending(a, b) ) ){
    var page_data = data.filter(d => d.page == p)
    .reduce( (obj, d) => {
      for(var r of REACTIONS){
        if(!obj[r]) obj[r] = {};
        if(!obj[r][d.category]) obj[r][d.category] = 0;
        obj[r][d.category] += d[r+'_count'];
      }
      if(!obj['post']) obj['post'] = {};
      if(!obj['post'][d.category]) obj['post'][d.category] = 0;
      obj['post'][d.category]++;
      return obj
    }, {})

    for(var r of Object.keys(page_data)){
      const category_counts = page_data[r];
      var max_count = [0,'']
      for(var c of Object.keys(category_counts)){
        if(max_count[0] < category_counts[c])
          max_count = [category_counts[c], c]
      }
      page_data[r] = {
        count: max_count[0],
        category: max_count[1]
      }
    }
    table_rows[p] = page_data
  }

  const t_headers = ['post', 'share', 'comment', 'like', 'love', 'wow', 'haha', 'sad', 'angry']
  const table = Table(table_rows, t_headers)
  container.node().appendChild( table.node() )

  return data
}

function buildCorrelationGraph(data){
  const container = d3.select('#correlations-container');
  const containerWidth = +container.style('width').slice(0, -2)
  const containerHeight = containerWidth / 1.63

  const graph = CorrelationGraph( containerWidth, containerHeight )
  graph.update( data )

  const correlation_select = Select( PAGES, 'All News Sources', 250 )
  
  const reaction_image_map = graph.reactions.reduce( (obj, r) => {
    obj[r] = `
      <img class='dropdown-icon' alt='${r}' src='https://peterandringa.com/facebook-news-analysis/img/reactions/${r}.png'/>
      - <span style="color:${REACTION_COLORS[r]}">${r}</span>
    `
    return obj
  }, {})

  const reaction_select = Select( reaction_image_map, 'All Reactions', 150 )


  var currentReactionFilter = false;
  reaction_select.addEventListener('change', e => {
    currentReactionFilter = e.value || false
    graph.update( currentData, currentReactionFilter )
  });

  var currentData = data
  correlation_select.addEventListener('change', e => {
    currentData = data.filter(d => !e.value || d.page == e.value )
    graph.update( currentData, currentReactionFilter )
  });

  d3.select('#correlations-select').node()
    .appendChild( correlation_select )

  d3.select('#correlations-select').node()
    .appendChild( reaction_select )

  container.node().appendChild( graph.svg )

  return data
}


function loadData(){
  return d3.csv("https://mj583.peterandringa.com/api/posts?from=2018-3-1&to=2018-3-15")
    .then(data => {
      return data.map(d => {
        d.like_count = +d.like_count
        d.love_count = +d.love_count
        d.wow_count = +d.wow_count
        d.haha_count = +d.haha_count
        d.sad_count = +d.sad_count
        d.angry_count = +d.angry_count
        d.comment_count = +d.comment_count
        d.share_count = +d.share_count
        // d.date = d3.timeParse("%Y-%m-%d %H:%M:%S%Z")(d.date)
        d.total_count = d.like_count + d.love_count + d.wow_count + d.haha_count + d.sad_count + d.angry_count
        return d
      })//.filter(d => d.total_likes && d.total_likes > 10 && d.comment_count && d.comment_count > 10)
    })
}

// MAIN CODE
const API_URL = 'https://mj583.peterandringa.com'
var pymParent = new pym.Parent('top_posts', API_URL+'/interactives/top_posts', {});

loadData()
  .then(data => {
    buildReactionBars(data)
    buildCategoryPies(data)
    buildCategoryTable(data)
    buildCorrelationGraph(data)
  })
