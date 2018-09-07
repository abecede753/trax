google.charts.load('current', {'packages':['corechart']});google.charts.setOnLoadCallback(drawChart);


// function drawChart() {
//     // Create the data table.
//     var data = new google.visualization.DataTable();
//     data.addColumn('string', 'Topping');
//     data.addColumn('number', 'Slices');
//     data.addRows([
//         ['Mushrooms', 10],
//         ['nions', 1],
//         ['Olives', 1],
//         ['Zucchini', 1],
//         ['Pepperoni', 2]
//     ]);
// 
//     // Set chart options
//     var options = {'title':'How Much Pizza I Ate Last Night',
//         'width':'100%',
//         'height':600};
// 
//     // Instantiate and draw our chart, passing in some options.
//     var chart = new google.visualization.BarChart(document.getElementById('chart_div'));
//     chart.draw(data, options);
// }


function drawChart() {
    var query = new google.visualization.Query(
        'https://docs.google.com/spreadsheets/d/19FzQ1IV4xmj41i-ShsL0XFeIx3QFleR50XihbYl_W5w/edit?usp=sharing&range=B:E');
    query.send(handleQueryResponse);
}

function handleQueryResponse(response) {
    if (response.isError()) {
        alert('Error in query: ' + response.getMessage() + ' ' + response.getDetailedMessage());
        return;
    }

    var data = response.getDataTable();
    var chart = new google.visualization.BarChart(document.getElementById('chart_div'));
    chart.draw(data, { height: 400 });
}

