/*************************
/* REACTION BARS
**************************/
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

/*************************
/* CATEGORY PIES
**************************/
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


/*************************
/* CATEGORY TABLE
**************************/
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


/*************************
/* CORRELATION GRAPH
**************************/
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


/*************************
/* LOAD DATA
**************************/
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

/*************************
/* MAIN
**************************/
const API_URL = 'https://mj583.peterandringa.com'
var pymParent = new pym.Parent('top_posts', API_URL+'/interactives/top_posts', {});

loadData()
  .then(data => {
    buildReactionBars(data)
    buildCategoryPies(data)
    buildCategoryTable(data)
    buildCorrelationGraph(data)
  });
