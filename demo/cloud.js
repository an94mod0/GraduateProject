<head>
<script src="http://d3js.org/d3.v3.min.js"></script>
<script src="http://yourjavascript.com/5414922491/cloud.js"></script>
<script
  src="https://code.jquery.com/jquery-3.4.1.js"
  integrity="sha256-WpOohJOqMqqyKL9FccASB9O0KwACQJpFTUBLTYOVvVU="
  crossorigin="anonymous"></script>
<script>
// require() method
const repositories = require('./data/wordcloud.json');
drawWordCloud(repositories);
// xhr method
var file_name="wordcloud.json"
var xhr = new XMLHttpRequest();
xhr.onreadystatechange = process;//非同步操作
xhr.open("GET",file_name, true);
xhr.send();//發送要求
function process(){
  console.log(xhr.status);
  if (xhr.readyState == 4) { //讀檔完成後執行
    //console.log(xhr.response);
  if(xhr.responseText=="")
    alert("file not found,check path");
  drawWordCloud(xhr.responseText);
  }
}

function drawWordCloud(tmp){
  var wordAndFreq={};
  var keys=Object.keys(tmp);
  for(var i=0;i<keys.length;++i){
    if(tmp[keys[i]]["draw"]){
      wordAndFreq[keys[i]]=tmp[keys[i]]["times"]+10.5;
    }
    else{
      wordAndFreq[keys[i]]=(tmp[keys[i]]["times"]|0); //必大於1
    }
  }
  var svg_location = "#cloud";
  var width = parseInt($("#cloud").css('width'));
  var height = parseInt($("#cloud").css('height'));
  var fill = d3.scale.category20(); // 顏色範圍 D3內定義的20種顏色 此處會隨機調用20種中其中一種為文字上色
  var linear_color = d3.scale.linear() // 自訂顏色範圍 根據權重比例決定顏色
      //.domain([0,1,2,3,4,5,6,10,15,20,100]) // 原本的資料範圍
      .domain([1,3,5,10,20,30,50,100])
      //.range(["#ddd", "#ccc", "#bbb", "#aaa", "#999", "#888", "#777", "#666", "#555", "#444", "#333", "#222"]);
      .range(["#222","#333","#444","#555","#666","#777","#888","#999","#aaa","#bbb","#ccc","#ddd"]); // 期望的資料範圍
  
  var ordinal_color = d3.scale.ordinal() // n個類別使用n種顏色
              .domain(0,0.1,0.2,0.3)
              .range(["#cc0000","#666666","#227700","#0000AA"]);
  var word_entries = d3.entries(wordAndFreq);

  var xScale = d3.scale.linear()
     .domain([0, d3.max(word_entries, function(d) {
        return d.value;
      })
     ])
     .range([12,72]);//字體的最小值與最大值

  d3.layout.cloud().size([width, height]) //設定尺寸
    .timeInterval(20)
    .words(word_entries) //所有詞打包
    .fontSize(function(d) { return xScale(+d.value); })
    .text(function(d) { return d.key; })
    //.rotate(function() { return ~~(Math.random() * 2) * 90; }) //只會旋轉0或90度
    .rotate(function() { return 0 }) //不旋轉
    //.rotate(function() { return (Math.random()-0.5)*180 ; }) // -180~180度間任意旋轉
    // ~~(x) 等價於 Math.floor(x) 但執行速度稍快
    .font("Impact")
    .on("end", draw)
    .start();
  function draw(words) {
    d3.select(svg_location).append("svg")
        .attr("width", width)
        .attr("height", height)
      .append("g")
        .attr("transform", "translate(" + [width >> 1, height >> 1] + ")")
      .selectAll("text")
        .data(words)
      .enter().append("text")
        .style("font-size", function(d) { return xScale(d.value) + "px"; })
        .style("font-family", "Impact")
        .on('click', function (d) {
          var idx=Math.floor(Math.random()*7);
          var audio=["v1-right.wav","v2-right.wav","v2-right.wav","v2-right.wav","v3-right.wav","v3-right.wav","v4-right.wav","v4-right.wav"]
          if(d.value%1==0.5){
              window.alert("關鍵字「"+d.key+"」出現"+(d.value-10.5)+"次\n來自"+audio[Math.floor(Math.random()*7)]);
          }
          else{
              window.alert("關鍵字「"+d.key+"」出現"+d.value+"次\n來自"+audio[Math.floor(Math.random()*7)]);
          }
          

        })
        .on('mouseover', function () { console.log($(this).text()); }   )
        .style("fill",function(d){if(d.value%1==0){
                                    return "hsl("+~~(Math.random()*360)+","+~~(Math.random()*70)+"%,60%)"
                                  }
                                  else if(d.value%1==0.5){ //med word
                                    return "hsl(0, 100%, 40%)";
                                  }
                                 })
        .attr("text-anchor", "middle")
        .attr("transform", function(d) {
          if(d.value%1==0){
              return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";
          }
          else{
              //return "translate(" + [d.x, d.y] + ")";
              return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";
          }
          
        })
        .text(function(d) { return d.key; });
      }
      d3.layout.cloud().stop();
  }
</script>
</head>
<body>
    <div id="cloud"></div>
</body>