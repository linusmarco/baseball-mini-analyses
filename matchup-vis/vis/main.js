var loadVis = function() {
    
    console.log("hi");

    var svg = d3.select("svg"),
        width = +svg.attr("width"),
        height = +svg.attr("height");

    var color = d3.scaleOrdinal()
        .domain([1,2])
        .range(["red", "blue"]);

    var simulation = d3.forceSimulation()
        .force("link", d3.forceLink().id(function(d) { return d.ID; }))
        .force("charge", d3.forceManyBody())
        .force("center", d3.forceCenter(width / 2, height / 2));

    d3.json("data/data.json", function(error, graph) {
        if (error) throw error;

        graph.nodes = graph.nodes.filter(function(n) { return n.ID !== "OTHER" });
        graph.links = graph.links.filter(function(l) { return l.source !== "OTHER" && l.target !== "OTHER" });

        graph.nodes = graph.nodes.map(function(n) {
            var node = n;
            var group = node.POS === "BATTER" ? 1 : 2;
            node.group = group;
            return node;
        });

        var link = svg.append("g")
            .attr("class", "links")
            .selectAll("line")
            .data(graph.links)
            .enter().append("line")
                .attr("stroke-width", function(d) { return d.PA; });

        var node = svg.append("g")
            .attr("class", "nodes")
            .selectAll("circle")
            .data(graph.nodes).enter()
            .append("circle")
                .attr("r", function(d) {
                    return d.PA / 50;
                })
                .attr("fill", function(d) { return color(d.group); })
                .call(d3.drag()
                    .on("start", dragstarted)
                    .on("drag", dragged)
                    .on("end", dragended));

        node.append("title")
            .text(function(d) { return d.ID; });

        simulation
            .nodes(graph.nodes)
            .on("tick", ticked);

        simulation.force("link")
            .links(graph.links);

        function ticked() {
            link
                .attr("x1", function(d) { return d.source.x; })
                .attr("y1", function(d) { return d.source.y; })
                .attr("x2", function(d) { return d.target.x; })
                .attr("y2", function(d) { return d.target.y; });

            node
                .attr("cx", function(d) { return d.x; })
                .attr("cy", function(d) { return d.y; });
        }
    });

    function dragstarted(d) {
        if (!d3.event.active) simulation.alphaTarget(0.3).restart();
        d.fx = d.x;
        d.fy = d.y;
    }

    function dragged(d) {
        d.fx = d3.event.x;
        d.fy = d3.event.y;
    }

    function dragended(d) {
        if (!d3.event.active) simulation.alphaTarget(0);
        d.fx = null;
        d.fy = null;
    }
}

document.addEventListener('DOMContentLoaded', loadVis, false);