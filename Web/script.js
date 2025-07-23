// DOM要素を取得
const container = document.getElementById("lab-container");

// 各研究室の最大収容人数
const maxCapacities = {
  harada_lab: 3,
};
// 研究室のJOSNリスト
const fileList = [
  "harada_lab.json"
];

// --- API通信関数 ---

// 個別の研究室データ(jsonファイル)を取得する関数
async function fetchLabData(filename) {
  const res = await fetch(`/${filename}`);
  if (!res.ok) throw new Error(`データファイル ${filename} の取得に失敗しました。`);
  return await res.json();
}

// --- 日付・時間計算ユーティリティ関数 ---

// 2つの日付文字列の差分を分単位で計算
function getDurationMinutes(startStr, endStr) {
  const start = new Date(startStr);
  const end = new Date(endStr);
  return Math.round((end - start) / 60000);
}

// 開始時間から現在までの経過時間を分単位で計算
function getMinutesSince(startStr) {
  const start = new Date(startStr);
  const now = new Date();
  return Math.round((now - start) / 60000);
}

// --- メイン処理 ---

// 研究室データを取得して画面表示を更新するメイン関数
async function updateLabs() {
  try {
    container.innerHTML = ""; // 表示コンテナを初期化

    for (const file of fileList) {
      const labData = await fetchLabData(file);
      const name = labData.lab_name || file.replace(".json", "");
      const data = labData.data || [];

      // 1. 滞在者と退出者を分類
      const inRoom = data.filter(d => !d.end);
      const exited = data.filter(d => d.end);
      const inRoomCount = inRoom.length;

      // 2. 混雑レベルを計算
      const maxCapacity = maxCapacities[name];
      const occupancyRate = inRoomCount / maxCapacity;
      let statusClass = "status-low"; // デフォルトは「空いている」
      if (occupancyRate >= 0.75) {
        statusClass = "status-high"; // 75%以上は「混雑」
      } else if (occupancyRate >= 0.4) {
        statusClass = "status-medium"; // 40%以上75%未満は「やや混雑」
      }
      
      const card = document.createElement("div");
      card.className = `lab-card ${statusClass}`;

      // 3. 共通の情報をHTMLに追加
      let innerHTML = `
        <h2>${name.charAt(0).toUpperCase() + name.slice(1)}</h2>
        <p>滞在者数: ${inRoomCount}人 / ${maxCapacity}人 (${Math.round(occupancyRate * 100)}%)</p>
      `;

      // 4. 過去の平均滞在時間を計算
      let avgStayMinutes = 0;
      if (exited.length > 0) {
        const totalDuration = exited.reduce((sum, d) => sum + getDurationMinutes(d.start, d.end), 0);
        avgStayMinutes = Math.round(totalDuration / exited.length);
        innerHTML += `<p>過去の平均滞在時間: 約 ${avgStayMinutes} 分</p>`;
      }
      
      // 5. 混雑緩和までの予想時間を計算（「混雑」または「やや混雑」の場合のみ）
      if (occupancyRate >= 0.4) {
        let nextLevelOccupancy;
        let targetStatus;

        if (occupancyRate >= 0.75) {
          // 「混雑」→「やや混雑」への緩和
          nextLevelOccupancy = Math.floor(0.75 * maxCapacity) - 1;
          targetStatus = "やや混雑";
        } else {
          // 「やや混雑」→「空いている」への緩和
          nextLevelOccupancy = Math.floor(0.4 * maxCapacity) - 1;
          targetStatus = "空いている";
        }

        if (inRoomCount > nextLevelOccupancy) {
          const peopleToLeave = inRoomCount - nextLevelOccupancy;
          const currentStays = inRoom.map(d => getMinutesSince(d.start)).sort((a, b) => b - a); // 長い順

          let totalEta = 0;
          for (let i = 0; i < peopleToLeave && i < currentStays.length; i++) {
            const timeUntilAvg = avgStayMinutes - currentStays[i];
            totalEta += Math.max(timeUntilAvg, 1); // 最低でも1分はかかると仮定
          }

          innerHTML += `<p><strong>${targetStatus}</strong>になるまでの予想時間: 約 <strong>${totalEta}</strong> 分</p>`;
        }
      }

      card.innerHTML = innerHTML;
      container.appendChild(card);
    }
  } catch (e) {
    container.innerHTML = `<p style="text-align: center; color: red;">データの更新に失敗しました: ${e.message}</p>`;
    console.error("更新時エラー:", e);
  }
}

// 初回更新を実行し、1分ごとに自動更新
updateLabs();
setInterval(updateLabs, 60000);
