#!/usr/bin/env python3
"""
腾讯会议 OpenClaw Skill 工具
支持基本的会议管理功能
"""

import os
import json
import time
import hashlib
import hmac
import base64
import requests
from urllib.parse import quote

class TencentMeetingTool:
    def __init__(self):
        self.token = os.getenv('TENCENT_MEETING_TOKEN')
        self.api_base = "https://api.meeting.qq.com"
        
        # 如果是简单的Bearer Token认证
        if self.token and len(self.token) > 30:
            self.auth_type = "bearer"
        else:
            # 如果是AK/SK格式
            self.secret_id = os.getenv('TENCENT_MEETING_SECRET_ID')
            self.secret_key = os.getenv('TENCENT_MEETING_SECRET_KEY')
            self.app_id = os.getenv('TENCENT_MEETING_APP_ID')
            self.sdk_id = os.getenv('TENCENT_MEETING_SDK_ID')
            self.auth_type = "aksk" if self.secret_id and self.secret_key else "unknown"
    
    def _generate_signature(self, method, uri, body="", timestamp=None, nonce=None):
        """生成TC3-HMAC-SHA256签名"""
        if not timestamp:
            timestamp = str(int(time.time()))
        if not nonce:
            nonce = str(int(time.time() * 1000000) % 1000000)
        
        # 构建签名字符串
        headers_str = f"X-TC-Key={self.secret_id}&X-TC-Nonce={nonce}&X-TC-Timestamp={timestamp}"
        string_to_sign = f"{method}\n{headers_str}\n{uri}\n{body}"
        
        # 计算HMAC-SHA256
        signature = hmac.new(
            self.secret_key.encode('utf-8'),
            string_to_sign.encode('utf-8'),
            hashlib.sha256
        ).digest()
        
        # 转换为16进制然后Base64编码
        hex_signature = ''.join(f'{b:02x}' for b in signature)
        final_signature = base64.b64encode(hex_signature.encode('utf-8')).decode('utf-8')
        
        return final_signature, timestamp, nonce
    
    def _make_request(self, method, endpoint, data=None):
        """发送API请求"""
        url = self.api_base + endpoint
        
        headers = {
            'Content-Type': 'application/json',
            'X-TC-Registered': '1'
        }
        
        if self.auth_type == "bearer":
            headers['Authorization'] = f'Bearer {self.token}'
        elif self.auth_type == "aksk":
            body_str = json.dumps(data) if data else ""
            signature, timestamp, nonce = self._generate_signature(
                method, endpoint, body_str
            )
            headers.update({
                'X-TC-Key': self.secret_id,
                'X-TC-Timestamp': timestamp,
                'X-TC-Nonce': nonce,
                'X-TC-Signature': signature,
                'AppId': self.app_id
            })
            if self.sdk_id:
                headers['SdkId'] = self.sdk_id
        
        try:
            if method.upper() == 'GET':
                response = requests.get(url, headers=headers, params=data)
            elif method.upper() == 'POST':
                response = requests.post(url, headers=headers, json=data)
            elif method.upper() == 'PUT':
                response = requests.put(url, headers=headers, json=data)
            elif method.upper() == 'DELETE':
                response = requests.delete(url, headers=headers, json=data)
            else:
                raise ValueError(f"Unsupported method: {method}")
            
            return response.json() if response.content else {}
        except Exception as e:
            return {"error": str(e), "status_code": getattr(response, 'status_code', 500)}
    
    def create_meeting(self, subject, start_time, end_time, host_id=None, attendees=None):
        """创建会议"""
        # 转换时间格式
        from datetime import datetime
        if isinstance(start_time, str):
            start_dt = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
        else:
            start_dt = start_time
        
        if isinstance(end_time, str):
            end_dt = datetime.fromisoformat(end_time.replace('Z', '+00:00'))
        else:
            end_dt = end_time
        
        # 计算会议时长（分钟）
        duration = int((end_dt - start_dt).total_seconds() / 60)
        
        meeting_data = {
            "subject": subject,
            "type": 0,  # 即时会议
            "hosts": [{"userid": host_id}] if host_id else [],
            "start_time": start_dt.strftime("%Y-%m-%dT%H:%M:%S"),
            "duration": duration,
            "settings": {
                "mute_enable_type": 1,  # 全体静音
                "allow_in_before_host": True,  # 允许成员在主持人进会前加入
                "auto_in_waiting_room": False,  # 不自动进入等候室
                "meeting_password": ""  # 无密码
            }
        }
        
        if attendees:
            meeting_data["invitees"] = [{"userid": user_id} for user_id in attendees]
        
        return self._make_request('POST', '/v1/meetings', meeting_data)
    
    def get_user_meetings(self, user_id, start_time=None, end_time=None):
        """获取用户会议列表"""
        params = {"userid": user_id}
        if start_time:
            params["start_time"] = start_time
        if end_time:
            params["end_time"] = end_time
        
        return self._make_request('GET', '/v1/meetings', params)
    
    def cancel_meeting(self, meeting_id, user_id, reason="取消会议"):
        """取消会议"""
        cancel_data = {
            "userid": user_id,
            "reason": reason
        }
        return self._make_request('POST', f'/v1/meetings/{meeting_id}/cancel', cancel_data)

# OpenClaw工具接口
def tencent_meeting_create(subject, start_time, end_time, host_id=None, attendees=None):
    """创建腾讯会议"""
    tool = TencentMeetingTool()
    return tool.create_meeting(subject, start_time, end_time, host_id, attendees)

def tencent_meeting_list(user_id, start_time=None, end_time=None):
    """列出腾讯会议"""
    tool = TencentMeetingTool()
    return tool.get_user_meetings(user_id, start_time, end_time)

def tencent_meeting_cancel(meeting_id, user_id, reason="取消会议"):
    """取消腾讯会议"""
    tool = TencentMeetingTool()
    return tool.cancel_meeting(meeting_id, user_id, reason)

if __name__ == "__main__":
    # 测试代码
    tool = TencentMeetingTool()
    print("Auth type:", tool.auth_type)
    print("Token length:", len(tool.token) if tool.token else 0)