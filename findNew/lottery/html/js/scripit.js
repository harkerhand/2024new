document.getElementById('stopLottery').disabled = true;

const intervalId = setInterval(generateWordCloud, 2000);

function generateWordCloud() {
    const names = students.map(student => student.name).join(' ');
    const canvas = document.getElementById('wordcloudCanvas');
    const nameArray = names.split(' ').map(name => [name, Math.floor(Math.random() * 11) + 6]);
    // console.log(nameArray);

    WordCloud(canvas, {
        list: nameArray,
        backgroundColor: '#222',
        color: (word, weight, fontSize, distance, theta) => {
            const colors = [
                '#FFFFFF', // 白色
                '#FFDD33', // 浅黄色
                '#33FF77', // 浅绿色
                '#33CCFF', // 浅蓝色
                '#FF3377', // 浅红色
                '#FF9933', // 橙色
                '#FF66FF', // 浅紫色
                '#FFD700', // 金色
            ];
            return colors[Math.floor(Math.random() * colors.length)]; // 随机选择颜色
        },
        weightFactor: 3, // 提高词的权重因子
        gridSize: 1, // 网格大小
        rotateRatio: 0.8, // 所有词汇都随机旋转
        shrinkToFit: true, // 适应画布
        drawOutOfBound: true, // 允许部分词汇绘制在画布外
        shape: 'square', // 词云形状
        fontFamily: '黑体', // 字体
    });

}

document.getElementById('startLottery').addEventListener('click', startLottery);
document.getElementById('stopLottery').addEventListener('click', stopLottery);

function getRandomWinners(numWinners) {
    const shuffled = students.sort(() => 0.5 - Math.random());
    return shuffled.slice(0, Math.min(numWinners, shuffled.length))
        .map(winner => `${winner.studentNumber}-${winner.name}`);
}

function showResult(results) {
    const resultDisplay = document.getElementById('resultDisplay');
    resultDisplay.innerHTML = '';
    results.forEach((result, index) => {
        if (index % 2 === 0) {
            const p = document.createElement('p');
            p.textContent = result;
            p.style.fontSize = '20px'; // 设置字体大小为20px
            resultDisplay.appendChild(p);
        } else {
            const lastP = resultDisplay.lastChild;
            lastP.textContent += `, ${result}`;
        }
    });
}

let numWinners;

let scrollInterval; // 定义一个变量存储滚动的间隔
function startLottery() {
    document.getElementById('stopLottery').disabled = false;
    document.getElementById('startLottery').disabled = true;
    document.getElementById('numWinners').disabled = true;

    numWinners = parseInt(document.getElementById('numWinners').value);
    if (isNaN(numWinners) || numWinners <= 0) {
        showResult(['请输入有效的抽奖人数！']);
        return;
    }

    scrollInterval = setInterval(() => {
        resultDisplay.innerHTML = ''; // 清空现有结果
        let winners = getRandomWinners(numWinners);
        showResult(winners);
    }, 100); // 每100毫秒更新一次
}


function stopLottery() {
    clearInterval(scrollInterval); // 清除滚动效果
    const winners = getRandomWinners(numWinners);
    numWinners = 0;
    showResult(winners);
    document.getElementById('stopLottery').disabled = true;
    document.getElementById('startLottery').disabled = false;
    document.getElementById('numWinners').disabled = false;
}
