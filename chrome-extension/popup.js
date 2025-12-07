const API_ENDPOINTS = {
    SMART_CLEANUP: 'http://localhost:8000/smart-cleanup'
  };
  
  const STATUS_TYPES = {
    LOADING: 'loading',
    SUCCESS: 'success',
    ERROR: 'error'
  };
  
  let isProcessing = false;
  
  async function collectAllTabs() {
    const tabs = await chrome.tabs.query({});
    const now = Date.now();
    
    return tabs.map(tab => ({
      id: tab.id,
      title: tab.title,
      url: tab.url,
      minutesAgo: Math.floor((now - tab.lastAccessed) / 60000)
    }));
  }
  
  async function collectActiveTabs() {
    const tabs = await chrome.tabs.query({active: true});
    const now = Date.now();
    
    return tabs.map(tab => ({
      id: tab.id,
      title: tab.title,
      url: tab.url,
      minutesAgo: Math.floor((now - tab.lastAccessed) / 60000)
    }));
  }
  
  function showStatus(message, type = '') {
    const status = document.getElementById('status');
    status.className = type;
    status.textContent = message;
  }
  
  // ============= API 호출 함수 =============
  
  async function requestSmartCleanup(focusedTabs, allTabs, timeThreshold) {
    const response = await fetch(API_ENDPOINTS.SMART_CLEANUP, {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({
        focused_tabs: focusedTabs,
        all_tabs: allTabs,
        time_threshold: timeThreshold
      })
    });
    
    if (!response.ok) {
      throw new Error(`서버 오류: ${response.status}`);
    }
    
    return await response.json();
  }
  

  document.getElementById('smartCleanup').addEventListener('click', async () => {
    if (isProcessing) return;
    
    isProcessing = true;
    const button = document.getElementById('smartCleanup');
    button.disabled = true;
    
    try {
      const timeThreshold = parseInt(document.getElementById('timeThreshold').value);
      
      if (!timeThreshold || timeThreshold < 1) {
        throw new Error('유효한 시간을 입력해주세요 (1분 이상)');
      }
      
      showStatus('🤖 현재 탭 분석 중...', STATUS_TYPES.LOADING);
      
      const activeTabs = await collectActiveTabs();
      
      if (activeTabs.length === 0) {
        throw new Error('활성 탭이 없습니다');
      }
      
      const allTabsData = await collectAllTabs();
      
      showStatus('🧠 AI가 컨텍스트 기반으로 분석 중...', STATUS_TYPES.LOADING);
      
      const result = await requestSmartCleanup(activeTabs, allTabsData, timeThreshold);
      
      if (!result.tab_ids || result.tab_ids.length === 0) {
        showStatus('✨ 정리할 탭이 없습니다!', STATUS_TYPES.SUCCESS);
        return;
      }
      
      const focusedTitles = activeTabs.map(t => t.title).join(', ');
      const confirmed = confirm(
        `현재 탭: ${focusedTitles}\n\n` +
        `${timeThreshold}분 이상 안 본 탭 중 ${result.tab_ids.length}개를 닫으시겠습니까?`
      );
      
      if (!confirmed) {
        showStatus('');
        return;
      }
      
      await chrome.tabs.remove(result.tab_ids);
      showStatus(`✅ ${result.tab_ids.length}개 탭 정리 완료!`, STATUS_TYPES.SUCCESS);
      
    } catch (error) {
      console.error('스마트 정리 오류:', error);
      showStatus(`❌ 오류: ${error.message}`, STATUS_TYPES.ERROR);
    } finally {
      button.disabled = false;
      isProcessing = false;
    }
  });