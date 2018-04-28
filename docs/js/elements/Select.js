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

class Select{
  constructor(choices, placeholder, width){
    // Image
    this.element = document.createElement('div')
    this.element.setAttribute('class', 'dropdown')
    if(width)
      this.element.setAttribute('style', 'width: '+width+'px')

    if(typeof choices == 'object'){
      choices = Object.keys(choices).map(k => ({
        id: k, text: choices[k]
      })).sort( (a,b) => d3.ascending(a.text, b.text) )
    }else{
      choices = choices.sort( (a,b) => d3.ascending(a, b) )
    }

    var singleInput = new Selectivity.Inputs.Single({
      element: this.element,
      items: choices,
      allowClear: true,
      placeholder: placeholder,
      templates: {
        resultItem: itemTemplate,
        singleSelectedItem: selectedTemplate
      },
    });
  }

  node() {
    return this.element
  }

  onChange(callback){
    this.element.addEventListener('change', callback)
  }
}