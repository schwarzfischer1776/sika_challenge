var cy = cytoscape({

    container: document.getElementById('cy'), // container to render in
    style: cytoscape.stylesheet()
    .selector('node')
      .style({
        'background-color': function( ele ){ return ele.data('bg')},  
        'label': function( ele ){ return ele.data('label'); }, 
        'font-family': function( ele ){ return ele.data('font-family')}

        // which works the same as

        // 'background-color': 'data(bg)'
      })
    }); 

    
function addNode() {
    cy.add({
        group: 'nodes',
        data: { weight: 75, label: "This is test sample ", 'font-family': 'Courier New' },
        position: { x: Math.random() * 500, y: Math.random() * 500 } // You can set the initial position here
    });
    }