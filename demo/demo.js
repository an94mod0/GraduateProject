import * as d3 from 'd3/build/d3';


import eventDrops from '../src';
import '../src/style.css';
import jQuery from 'jquery';
import Chart from 'chart.js';

//import CanvasJS from 'canvasjs';
function switchMenu( theMainMenu, theSubMenu, theEvent ){
    var SubMenu = document.getElementById( theSubMenu );
    if( SubMenu.style.display == 'none' ){ // 顯示子選單
        SubMenu.style.minWidth = theMainMenu.clientWidth; // 讓子選單的最小寬度與主選單相同 (僅為了美觀)
        SubMenu.style.display = 'block';
        hideMenu(); // 隱藏子選單
        VisibleMenu = theSubMenu;
    }
    else{
        if( theEvent != 'MouseOver' || VisibleMenu != theSubMenu ){
            SubMenu.style.display = 'none';
            VisibleMenu = '';
        }
    }
}

// 隱藏子選單
function hideMenu(){
    if( VisibleMenu != '' ){
        document.getElementById( VisibleMenu ).style.display = 'none';
    }
    VisibleMenu = '';
}



window.$ = window.jQuery = jQuery;
$( document ).ready(function() {
    $("#flip").click(function(){
        $("#panel").slideToggle("normal");
    });
    //console.log($("#emo_radar"));
    //console.log("ready");
    const repositories = require('./data/wordcloud.json');
    drawWordCloud(repositories);

    drawRadar([[303,30,148,9,168,150],[400,115,202,33,28,30]]);
});
Chart.defaults.global.defaultFontSize=18;
function drawRadar(emotion_count){
    var ctx = document.getElementById('c1').getContext('2d');
        var myRadarChart = new Chart(ctx, {

            type: 'radar',
            data: {
              labels: ["calm","happy","sad","angry","fearful","disgust"],
              datasets: [
              {
                label: 'A',
                backgroundColor:'rgba(255,20,20,0.5)',
                data: [303,30,148,9,168,150]
              },{
                label: 'B',
                backgroundColor:'rgba(20,20,255,0.5)',
                data: [400,115,202,33,28,30]
              },{
                label: 'C',
                backgroundColor:'rgba(66, 244, 122,0.5)',
                data: [250,200,100,60,78,50]
              }]
            },
            options: {
                legend:{
                    labels:{
                        //fontSize:32
                    }
                },
                scale: {
                    pointLabels: {
                        fontSize: 22,
                    }
                }
            }
        });
    var ctx2 = document.getElementById('c2').getContext('2d');
        var myRadarChart = new Chart(ctx2, {
            type: 'radar',
            data: {
              labels: ["calm","happy","sad","angry","fearful","disgust"],
              datasets: [
              {
                label: 'A',
                backgroundColor:'rgba(255,20,20,0.5)',
                data: [200,40,100,120,40,180]
              },{
                label: 'B',
                backgroundColor:'rgba(20,20,255,0.5)',
                data: [130,30,320,10,180,270]
              }]
            },
            options: {
                legend:{
                    labels:{
                        //fontSize:32
                    }
                },
                scale: {
                    pointLabels: {
                        fontSize: 22,
                    }
                }
            }
        });
}


function humanizeDate(date){
    const monthNames = [
        'Jan.',
        'Feb.',
        'March',
        'Apr.',
        'May',
        'June',
        'Jul.',
        'Aug.',
        'Sept.',
        'Oct.',
        'Nov.',
        'Dec.',
    ];
    if(date.getSeconds()==57){
        return `${date.getMinutes()}:${date.getSeconds()}~${date.getMinutes()+1}:0`;
    }
    else{
        return `${date.getMinutes()}:${date.getSeconds()}~${date.getMinutes()}:${(date.getSeconds()+3)%60}`;
    }
    
}
function eventdrops(){
    const repositories = require('./data/eventdrops.json'); //視覺化用的資料
    const numberCommitsContainer = document.getElementById('numberCommits');
    const zoomStart = document.getElementById('zoomStart');
    const zoomEnd = document.getElementById('zoomEnd');
    const updateCommitsInformation = chart => { //捲動功能
        const filteredData = chart
            .filteredData()
            .reduce((total, repo) => total.concat(repo.data), []);
        numberCommitsContainer.textContent = filteredData.length;
        zoomStart.textContent = humanizeDate(chart.scale().domain()[0]);
        zoomEnd.textContent = humanizeDate(chart.scale().domain()[1]);
    };

    const tooltip = d3 //mouseover時的懸浮資訊窗
        .select('body')
        .append('div')
        .classed('tooltip', true)
        .style('opacity', 0)
        .style('pointer-events', 'auto');

    const chart = eventDrops({ //設定繪製參數
        d3,
        zoom: {
            onZoomEnd: () => updateCommitsInformation(chart),
        },
        drop: {
            date: d => new Date(d.date),
            onMouseOver: commit => { //出現關鍵字與時間
                tooltip
                    .transition()
                    .duration(200)
                    .style('opacity', 1)
                    .style('pointer-events', 'auto');

                tooltip
                    .html(
                        `
                        <div class="commit">
                        <div class="content">
                            <h3 class="message">醫療關鍵字:${commit.message}</h3>
                            <p>
                                on <span class="date">${humanizeDate(
                                    new Date(commit.date)
                                )}</span>
                            </p>
                        </div>
                    `
                    )
                    .style('left', `${d3.event.pageX - 30}px`)
                    .style('top', `${d3.event.pageY + 20}px`);
            },
            onMouseOut: () => {
                tooltip
                    .transition()
                    .duration(500)
                    .style('opacity', 0)
                    .style('pointer-events', 'none');
            },
        },
    });
    const repositoriesData = repositories.map(repository => ({
        name: repository.name,
        data: repository.data,
    }));
    d3.select('#eventdrops').data([repositoriesData]).call(chart); //繪製
    updateCommitsInformation(chart);
}


//import { writeFileSync, readFileSync } from 'fs';
//const path = require('path');
/*
const walk = async (dir, filelist = []) => {
  const files = await fs.readdir(dir);

  for (file of files) {
    const filepath = path.join(dir, file);
    const stat = await fs.stat(filepath);

    if (stat.isDirectory()) {
      filelist = await walk(filepath, filelist);
    } else {
      filelist.push(file);
    }
  }
  return filelist;
}
console.log(walk('./data'));
*/

$('input[type="range"]').val(10).change();

eventdrops();
