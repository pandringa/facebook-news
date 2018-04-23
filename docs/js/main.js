const CATEGORIES = ['national','politics','business','science','world','sports','lifestyle','opinion']
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

function buildSelect(choices, placeholder, width){
  var element = document.createElement('div')
  element.setAttribute('class', 'dropdown')
  element.setAttribute('style', 'width: '+width+'px')

  if(typeof choices == 'object'){
    choices = Object.keys(choices).map(k => ({
      id: k, text: choices[k]
    }))
  }

  var singleInput = new Selectivity.Inputs.Single({
    element: element,
    items: choices,
    allowClear: true,
    placeholder: placeholder
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
    console.log(bars.svg.node())
    container.node().appendChild(bars.svg.node())
    category_bars.push( bars )
  }

  // const category_select = buildSelect( CATEGORIES, 'All Categories', 170 )
  const page_select = buildSelect( PAGES, 'All News Sources', 250 )
  d3.select('#reaction-selects').node()
    .appendChild(page_select)
  
  page_select.addEventListener('change', e => {
    category_bars.forEach(b => {
      const newData = data.filter(d => d.title == b.category && (!e.value || d.page == e.value) )
      console.log(e.value, b.title, data, newData)
      b.update( newData )
    })
  });
}


function loadData(){
  return d3.csv("https://mj583.peterandringa.com/api/posts?from=2018-3-1&to=2018-3-7")
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
  .then(buildReactionBars)
