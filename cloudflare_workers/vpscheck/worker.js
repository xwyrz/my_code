// 配置部分 - 根据你的情况修改这些值
const config = {
  // 要监控的产品列表
  PRODUCTS: [
      {
          name: "HK-T1",
          url: "https://my.rfchost.com/index.php?rp=/store/hk-tier-1-international-optimization-network/t1ion-unlimited-speed-balance",
          keywords: {
              outOfStock: ["Out of Stock", "out of stock", "currently out of stock"],
              inStock: ["Continue"]
          }
      },
      {
          name: "HK-T1-Jinx",
          url: "https://my.rfchost.com/index.php?rp=/store/hk-tier-1-international-optimization-network-jinx/t1ion-unlimited-speed-balance-jinx",
          keywords: {
              outOfStock: ["Out of Stock", "out of stock", "currently out of stock"],
              inStock: ["Continue"]
          }
      },
      {
          name: "JP-T1",
          url: "https://my.rfchost.com/index.php?rp=/store/jp-tier-1-international-optimization-network/jp-t1ion-balance",
          keywords: {
            outOfStock: ["Out of Stock", "out of stock", "currently out of stock"],
            inStock: ["Continue"]
          }
      }
  ],
  
  // Telegram 配置
  TELEGRAM_BOT_TOKEN: '11011hiBo',
  TELEGRAM_CHAT_ID: '8205',
  
  // 请求超时时间(毫秒)
  TIMEOUT: 5000
};

// 主处理函数 - 监控单个产品
async function monitorProduct(product) {
  let response;
  let status = 'unknown';
  let errorMessage = '';
  let pageContent = '';
  let isInStock = false;
  
  try {
      // 创建带超时的fetch请求
      const controller = new AbortController();
      const timeout = setTimeout(() => controller.abort(), config.TIMEOUT);
      
      response = await fetch(product.url, {
          signal: controller.signal
      });
      clearTimeout(timeout);
      
      // 获取页面内容
      pageContent = await response.text();
      
      // 检查是否缺货
      const isOutOfStock = product.keywords.outOfStock.some(keyword => 
          pageContent.includes(keyword)
      );
      
      // 检查是否有货
      const isInStockDetected = product.keywords.inStock.some(keyword =>
          pageContent.includes(keyword)
      );
      
      // 确定库存状态
      if (isOutOfStock && !isInStockDetected) {
          status = 'out_of_stock';
      } else if (isInStockDetected) {
          status = 'in_stock';
          isInStock = true;
      } else {
          status = 'unknown_stock_status';
          errorMessage = '无法确定库存状态 - 页面内容不符合预期';
      }
      
  } catch (error) {
      status = 'error';
      errorMessage = error.message;
  }
  
  return {
      productName: product.name,
      status,
      isInStock,
      error: errorMessage || null,
      url: product.url,
      timestamp: new Date().toISOString()
  };
}

// 发送Telegram通知
async function sendTelegramNotification(message) {
  const url = `https://api.telegram.org/bot${config.TELEGRAM_BOT_TOKEN}/sendMessage`;
  
  try {
      const response = await fetch(url, {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json'
          },
          body: JSON.stringify({
              chat_id: config.TELEGRAM_CHAT_ID,
              text: message,
              disable_notification: false,
              parse_mode: 'HTML'
          })
      });
      
      const data = await response.json();
      if (!data.ok) {
          console.error('Telegram API错误:', data);
      }
  } catch (error) {
      console.error('发送Telegram通知失败:', error);
  }
}

// 处理所有产品监控
async function handleAllProducts() {
  const results = [];
  
  // 依次监控所有产品
  for (const product of config.PRODUCTS) {
      const result = await monitorProduct(product);
      results.push(result);
      
      // 准备通知消息
      let message = `<b>🖥 VPS库存监控通知</b>\n\n`;
      message += `<b>📦 产品:</b> ${result.productName}\n`;
      message += `<b>🌐 页面:</b> <a href="${result.url}">查看产品</a>\n`;
      message += `<b>🕒 时间:</b> ${result.timestamp}\n`;
      
      if (result.isInStock) {
          message += `<b>🟢 状态:</b> <u>有货! 快去抢购!</u>\n`;
          message += `🚀 产品已补货，立即购买!\n`;
          
          // 发送通知
          await sendTelegramNotification(message);
          
          // 有货时可以发送额外的提醒
          const alertMessage = `🚨 <b>紧急: ${result.productName} 已补货!</b>\n<a href="${result.url}">立即购买</a>`;
          await sendTelegramNotification(alertMessage);
      } else if (result.status === 'out_of_stock') {
          message += `<b>🔴 状态:</b> 缺货\n`;
          message += `😞 产品暂时缺货，继续监控中...\n`;
          
          // 缺货时可以选择不发送通知，或者只在调试时发送
          // await sendTelegramNotification(message);
      } else {
          message += `<b>🟡 状态:</b> ${result.status}\n`;
          if (result.error) {
              message += `⚠️ 错误: ${result.error}\n`;
          }
          // 未知状态时发送通知以便检查
          //await sendTelegramNotification(message);
      }
  }
  
  return results;
}

// Worker入口
export default {
  async fetch(request, env, ctx) {
      const results = await handleAllProducts();
      return new Response(JSON.stringify(results, null, 2), {
          headers: { 'Content-Type': 'application/json' },
          status: 200
      });
  },
  
  async scheduled(event, env, ctx) {
      ctx.waitUntil(handleAllProducts());
  }
};
