var loadVis = function() {
    
    console.log("hi");

    var svg = d3.select("svg"),
        width = +svg.attr("width"),
        height = +svg.attr("height");

    var colorPos = d3.scaleOrdinal()
        .domain([1,2])
        .range(["red", "blue"]);

    var simulation = d3.forceSimulation()
        .force("link", d3.forceLink().id(function(d) { return d.ID; }))
        .force("charge", d3.forceManyBody())
        .force("center", d3.forceCenter(width / 2, height / 2));



    d3.json("data/data.json", function(error, graph) {
        if (error) throw error;

        var mean = graph.summary.OPS.mean;
        var std = graph.summary.OPS.std;

        var colorMeas = d3.scaleLinear()
            .domain([0, (mean - 2*std), (mean - std), mean, (mean + std), (mean + 2*std), 5])
            .range(["#0000ff", "#1313FB", "#4D4DEF", "lightgray", "#EF4D4D", "#FB1313", "#FF0000"]);

        graph.nodes = graph.nodes.filter(function(n) { return n.ID !== "OTHER" });
        graph.links = graph.links.filter(function(l) { return l.source !== "OTHER" && l.target !== "OTHER" });

        graph.nodes = graph.nodes.map(function(n) {
            var node = n;
            var group = node.POS === "BATTER" ? 1 : 2;
            node.group = group;
            return node;
        });

        var yScale = d3.scaleLinear()
            .domain([0, 19])
            .range([25, 725]);

        var link = svg.append("g")
            .attr("class", "links")
            .selectAll("line")
            .data(graph.links)
            .enter().append("line")
                .style("stroke-width", function(d) { return d.PA; })
                .style("stroke", function(d) { return colorMeas(d.OPS); });


        var pitchers = graph.nodes.filter(function(d) { return d.POS === "PITCHER" });
        var nodesPitch = svg.append("g")
            .attr("class", "pitchers")
            .selectAll("circle")
            .data(pitchers).enter()
            .append("circle")
                .attr("cx", 25)
                .attr("cy", function(d, i) {
                    return yScale(i);
                })
                .attr("r", function(d) {
                    return d.PA / 50;
                })
                .attr("fill", function(d) { return colorPos(d.group); })
                .style("stroke", "black")
                .style("stroke-width", 0.5)

        var batters = graph.nodes.filter(function(d) { return d.POS === "BATTER" });
        var nodesBat = svg.append("g")
            .attr("class", "batters")
            .selectAll("circle")
            .data(batters).enter()
            .append("circle")
                .attr("cx", 800)
                .attr("cy", function(d, i) {
                    return yScale(i);
                })
                .attr("r", function(d) {
                    return d.PA / 50;
                })
                .attr("fill", function(d) { return colorPos(d.group); })
                .style("stroke", "black")
                .style("stroke-width", 0.5)

        // node.append("title")
        //     .text(function(d) { return d.ID; });

    });

}

document.addEventListener('DOMContentLoaded', loadVis, false);