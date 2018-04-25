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
