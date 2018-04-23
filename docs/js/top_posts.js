var pymChild = new pym.Child();

const tabs = d3.selectAll('li.tab')

tabs.on('click', () => {
  d3.selectAll('.current').classed('current', false)

  var target = d3.event.target
  while(target.nodeName != 'LI')
    target = target.parentNode;
  
  const reaction = d3.select(target)
    .classed('current', true)
    .attr('data-reaction')

  d3.select(`.post[data-reaction="${reaction}"]`)
    .classed('current', true)
})

window.fbAsyncInit = function() {
  FB.XFBML.parse(null, () => pymChild.sendHeight() );
};