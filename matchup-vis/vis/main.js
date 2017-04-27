var loadVis = function() {
    
    var svg = d3.select("svg"),
        margin = {top: 20, right: 20, bottom: 30, left: 40},
        width = +svg.attr("width") - margin.left - margin.right,
        height = +svg.attr("height") - margin.top - margin.bottom,
        g = svg.append("g").attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    var divisions = d3.scaleBand()
        .rangeRound([0, height])
        .paddingInner(0.1);

    var players = d3.scaleBand()
        .padding(0.05);

    d3.csv("../matchups.csv", function(data) {
        console.log(data);
    })
}

document.addEventListener('DOMContentLoaded', loadVis, false);