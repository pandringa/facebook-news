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