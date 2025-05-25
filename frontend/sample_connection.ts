import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class WebSocketService {
  private socket: WebSocket;

  constructor() {
    this.socket = new WebSocket('wss://<API_ID>.execute-api.<REGION>.amazonaws.com/<STAGE>');

    this.socket.onopen = () => {
      console.log('WebSocket connection established.');
      this.sendMessage('Hello from Angular!');
    };

    this.socket.onmessage = (event) => {
      console.log('Received:', event.data);
    };

    this.socket.onclose = (event) => {
      console.log('WebSocket connection closed:', event);
    };

    this.socket.onerror = (error) => {
      console.error('WebSocket error:', error);
    };
  }

  sendMessage(message: string) {
    const payload = {
      action: 'sendmessage',
      message: message
    };
    this.socket.send(JSON.stringify(payload));
  }
}
