# 🤖 LARP.ai — LLM Assisted Robotics Platform
### Retrofit Any Machine with Language Intelligence · MCP-Native · Industry 4.0 Ready
 
[![Platform](https://img.shields.io/badge/platform-Raspberry%20Pi-red)]()
[![Protocol](https://img.shields.io/badge/protocol-FastMCP-blue)]()
[![LLM](https://img.shields.io/badge/LLM-Ollama%20%7C%20Cloud-green)]()
[![Language](https://img.shields.io/badge/language-Python-yellow)]()
 
---
 
> LARP.ai is a modular LLM-based assistant system that retrofits legacy industrial machines with AI intelligence — no hardware replacement required. Powered by Model Context Protocol (MCP), it bridges natural language instructions to real-world tool execution, enabling any "dumb" machine to become a smart, AI-driven system.
 
---
 
## 💡 The Problem
 
As Industry 4.0 accelerates, supply chains are shifting from manual-operated equipment to autonomous AI-driven machinery — like the robotic systems seen in Amazon fulfilment centres. But **not every industry can afford a full hardware overhaul**.
 
LARP.ai solves this by retrofitting existing machines with a Raspberry Pi running an MCP server. The Pi takes over what was previously a human operator's input — sending execution commands directly to the machine's onboard microcontroller.
 
Every robot or piece of machinery already has a microcontroller at its core — in LARP's reference implementation, an **ESP32** — which accepts execution commands and internally drives whatever sub-components the machine needs (motor controllers, actuators, servos, etc.). That ESP32 was designed to receive commands from a human operator via a physical controller. LARP simply lets the Pi send those same commands instead, under LLM direction.
 
---
 
## 🧠 Architecture
 
LARP.ai supports two deployment architectures depending on the industry's needs:
 
### Architecture 1 — Cloud Inference (Managed Service) ☁️
 
```
 ┌──────────────────────────────────────────────────────────────────────────┐
 │ CLOUD                                                                    │
 │                                                                          │
 │  ┌─────────────────────────────────────────────────────────────────────┐ │
 │  │ MCP HOST  (e.g. Claude Desktop)                                     │ │
 │  │                                                                     │ │
 │  │  ┌──────────────────────────┐      ┌──────────────────────────────┐ │ │
 │  │  │ LLM                      │      │ MCP CLIENT                   │ │ │
 │  │  │ · parse user prompt      │─────▶│ · tools/list  (on connect)   │ │ │
 │  │  │ · reason about task      │      │ · tools/call  (on decision)  │ │ │
 │  │  │ · decide which tool      │◀─────│ · relay tool_result to LLM   │ │ │
 │  │  │ · generate final answer  │      └──────────────┬───────────────┘ │ │
 │  │  └──────────────────────────┘                     │                 │ │
 │  └───────────────────────────────────────────────────│─────────────────┘ │
 └─────────────────────────────────────────────────────-│───────────────────┘
                                                        │
                                          JSON-RPC 2.0 over HTTP / SSE
                                          { "method": "tools/call",
                                            "params": { "name": "move_forward",
                                                        "arguments": {} }}
                                                        │
 ┌──────────────────────────────────────────────────────│───────────────────┐
 │ RASPBERRY PI  (on-robot)                             │                   │
 │                                                      ▼                   │
 │  ┌──────────────────────────────────────────────────────────────────┐    │
 │  │ MCP SERVER  (FastMCP)                                            │    │
 │  │                                                                  │    │
 │  │  ┌───────────────────────────────────────────────────────────┐   │    │
 │  │  │ TOOL REGISTRY  (actual tools from codebase)               │   │    │
 │  │  │                                                           │   │    │
 │  │  │  movement.py   @tool move_forward()                       │   │    │
 │  │  │                @tool move_backward()                      │   │    │
 │  │  │                @tool turn_left()                          │   │    │
 │  │  │                @tool turn_right()                         │   │    │
 │  │  │                @tool turn_180()                           │   │    │
 │  │  │                @tool turn_360()                           │   │    │
 │  │  │                                                           │   │    │
 │  │  │  head.py       @tool head_up / down / left / right()      │   │    │
 │  │  │                @tool head_center()                        │   │    │
 │  │  │                @tool nod_yes / nod_no()                   │   │    │
 │  │  │                                                           │   │    │
 │  │  │  speech.py     @tool speak(text, eye_expression)          │   │    │
 │  │  │  expression.py @tool default_eyes()                       │   │    │
 │  │  │  vision.py     @tool list_objects_in_image()              │   │    │
 │  │  │  general.py    @tool reset_bot_activity()                 │   │    │
 │  │  └──────────────────────┬──────────────────┬───────────-─────┘   │    │
 │  │                         │                  │                     │    │
 │  │              hardware tools           vision tool                │    │
 │  │                         │                  │                     │    │
 │  │                         ▼                  ▼                     │    │
 │  │  ┌──────────────────────────┐   ┌──────────────────────────-─┐   │    │
 │  │  │ hardware/motors.py       │   │ vision.py                  │   │    │
 │  │  │ hardware/servos.py       │   │ · capture frame (picam2)   │   │    │
 │  │  │                          │   │ · POST image over HTTP     │   │    │
 │  │  │ ser.write("FORWARD\n")   │   │   to CV server             │   │    │
 │  │  │ ser.write("HEAD_UP\n")   │   │ · merge detection results  │   │    │
 │  │  │ → /dev/ttyUSB0           │   │ · return objects list      │   │    │
 │  │  │   115200 baud            │   └──────────┬────────────────-┘   │    │
 │  │  └──────────┬───────────────┘              │ HTTP POST           │    │
 │  └─────────────│──────────────────────────────│───────────────────-─┘    │
 └───────────────-│──────────────────────────────│───────────────────-──────┘
                  │ USB Serial                   │ LAN  (10.222.138.220:5001)
                  │ plain text commands          │
                  ▼                              ▼
 ┌───────────────────────────┐    ┌──────────────────────────────────────┐
 │ ESP32                     │    │ CV SERVER  (separate machine on LAN) │
 │ (Robot Microcontroller)   │    │ · receives JPEG over HTTP            │
 │ · receives "FORWARD\n"    │    │ · runs object detection model        │
 │ · runs motor firmware     │    │ · returns { objects, count }         │
 │ · drives L298N / servo    │    └──────────────────────────────────────┘
 │   drivers internally      │
 └───────────────────────────┘
```
 
> **Note on the CV server:** it is a plain HTTP service (not an MCP server). The Pi calls it internally as part of the `list_objects_in_image` MCP tool — the LLM only ever sees one unified MCP interface on the Pi.
 
---
 
### Architecture 2 — LAN Self-Hosted (Fully Independent) 🏭
 
```
 ┌────────────────────────────────────────────────────────────────────────────┐
 │ FACILITY LAN                                                               │
 │                                                                            │
 │  ┌───────────────────────────────────────────────────────────────────────┐ │
 │  │ LAN INFERENCE SERVER  (dedicated on-premises machine)                 │ │
 │  │                                                                       │ │
 │  │  ┌──────────────────────┐    ┌──────────────────────────────────────┐ │ │
 │  │  │ Ollama + Mistral 7B  │    │ MCP CLIENT LAYER                     │ │ │
 │  │  │                      │◀──▶│ · tools/list on connect to each Pi   │ │ │
 │  │  │ · prompt parsing     │    │ · tools/call when action decided     │ │ │
 │  │  │ · tool selection     │    │ · route call to correct Pi server    │ │ │
 │  │  │ · response gen       │    └──────────┬─────────────┬─────────────┘ │ │
 │  │  └──────────────────────┘               │             │               │ │
 │  └─────────────────────────────────────────│─────────────│───────────────┘ │
 │                                            │             │                 │
 │                              JSON-RPC 2.0  │             │  JSON-RPC 2.0   │
 │                              over HTTP/SSE │             │  over HTTP/SSE  │
 │                                            ▼             ▼                 │
 │  ┌─────────────────────────────────────┐      ┌──────────────────────────┐ │
 │  │ RASPBERRY PI #1  (MCP Server)       │      │ RASPBERRY PI #2 (MCP Svr)│ │
 │  │                                     │      │                          │ │
 │  │ Tool Registry:                      │      │ Tool Registry:           │ │
 │  │  @tool move_forward()               │      │  @tool move_forward()    │ │
 │  │  @tool turn_left / right()          │      │  @tool turn_left()  ...  │ │
 │  │  @tool head_up / down()             │      │  (same or different      │ │
 │  │  @tool speak(text, expression)      │      │   tools per machine)     │ │
 │  │  @tool list_objects_in_image()      │      │                          │ │
 │  │  @tool reset_bot_activity()  ...    │      │                          │ │
 │  │         ↓                           │      │         ↓                │ │
 │  │  motors.py / servos.py              │      │  motors.py / servos.py   │ │
 │  │  ser.write("CMD\n")                 │      │  ser.write("CMD\n")      │ │
 │  │  → /dev/ttyUSB0 @ 115200            │      │  → /dev/ttyUSB0 @ 115200 │ │
 │  └──────────────────┬──────────────────┘      └────────────┬─────────────┘ │
 │                     │ USB Serial                           │ USB Serial    │
 │                     ▼                                      ▼               │
 │              ┌────────────┐                         ┌────────────┐         │
 │              │  ESP32 #1  │                         │  ESP32 #2  │         │
 │              │  (Robot A) │                         │  (Robot B) │  ...    │
 │              └────────────┘                         └────────────┘         │
 │                                                                            │
 │  ┌────────────────────────────────────────────────────────────────────-─┐  │
 │  │ CV SERVER  (shared, HTTP)  ← called by both Pis via requests.post    │  │
 │  │ 10.222.138.220:5001/detect                                           │  │
 │  └────────────────────────────────────────────────────────────────────-─┘  │
 └────────────────────────────────────────────────────────────────────────----┘
```
 
In both architectures, **the Raspberry Pi is always the MCP Server** — it exposes all robot capabilities as MCP tools and translates tool calls into plain-text serial commands sent to the ESP32 over USB (`/dev/ttyUSB0`, 115200 baud). The LLM never speaks directly to hardware — it only speaks MCP.
 
---
 
## ⚙️ How It Works
 
```
User gives task in plain English
          │
          ▼
┌──────────────────────────┐
│  LLM (Cloud or LAN)      │
│  MCP Client              │
│  · Parses intent         │
│  · Selects tool to call  │
│  · Generates parameters  │
└──────────┬───────────────┘
           │ MCP tool call
           ▼
┌──────────────────────────┐
│  Raspberry Pi            │
│  MCP Server              │
│  · Receives tool call    │
│  · Translates to command │
│  · Sends to ESP32        │
└──────────┬───────────────┘
           │ execution command
           ▼
┌──────────────────────────┐
│  ESP32                   │
│  Machine Microcontroller │
│  · Receives command      │
│  · Drives sub-components │
│    (motors, actuators…)  │
└──────────┬───────────────┘
           │ result / feedback
           ▼
┌──────────────────────────┐
│  LLM                     │
│  · Incorporates result   │
│  · Refines if needed     │
│  · Returns final response│
└──────────────────────────┘
```
 
The LLM supports **multi-step reasoning** — it can iteratively call tools, observe results, and refine its approach before producing a final output.
 
---
 
## 🧩 System Components
 
### `pi-mcp-server/`
The core MCP server running on the Raspberry Pi. Hosts all tool definitions — each tool maps a high-level action (e.g. "move forward") to the exact execution command the machine's ESP32 expects. When the LLM decides to call a tool, the Pi translates that into a direct command to the ESP32, which then handles everything internally (driving motors, actuators, etc.). This is the critical bridge between AI intent and physical action.
 
### `cv-server/`
A separate MCP-compatible Computer Vision server. Handles image-based tasks such as visual understanding and scene processing. Runs as an independent service and is callable by the LLM via MCP just like any other tool.
 
---
 
## 🏗️ Tech Stack
 
| Layer | Technology |
|---|---|
| Orchestration | Raspberry Pi 3/4B |
| Machine Microcontroller | ESP32 |
| MCP Framework | FastMCP |
| LAN Inference | Ollama + Mistral 7B |
| Cloud Inference | Claude (via MCP Desktop) |
| Vision | OpenCV / custom CV server |
| Language | Python |
 
---
 
## 🔄 Deployment Architectures
 
### Architecture 1 — Cloud Inference ☁️
 
- Industry pays a small monthly subscription for cloud LLM inference
- **Lower setup cost**, higher running cost
- Best performance — demonstrated with Claude Desktop MCP integration
- Latency is present due to network roundtrip
- Ideal for: industries wanting quick adoption with minimal infrastructure
### Architecture 2 — LAN Self-Hosted 🏭
 
- Industry runs their own Ollama inference server on-premises
- **Higher setup cost**, near-zero running cost
- Multiple Raspberry Pi clients (one per machine) connect to the same LAN LLM server
- Fully self-dependent — no external dependency or data leaving the facility
- Demonstrated with Mistral 7B; model quality scales with server hardware
- Ideal for: industries prioritising data sovereignty and long-term cost efficiency
---
 
## 🔌 Adding a New Machine
 
To integrate a new machine into LARP.ai, you only need to:
 
1. Attach a Raspberry Pi to the machine and connect it to the ESP32
2. Define MCP tools for the machine's actions — each tool wraps the command the ESP32 expects for that action
3. Point the Pi's MCP server at your LLM server (cloud or LAN)
4. Assign the LLM a task in plain English — it handles the rest
No new model training. No changes to the ESP32's firmware or internal wiring.
 
---
 
## ✨ Key Design Principles
 
**Decoupled Architecture** — Each capability (LLM, vision, future tools) runs as an independent server. They can be updated, swapped, or scaled independently.
 
**Extensibility** — New tools are added by spinning up additional MCP-compatible services. The LLM automatically discovers and routes to them.
 
**Local-First by Default** — The entire pipeline can run on local infrastructure, keeping sensitive operational data within the facility.
 
**Hardware Agnostic** — LARP.ai doesn't care what machine it's controlling. As long as you can define the controller's request codes as MCP tools, it works.
 
**Standardised Tool Interface** — All tool invocation follows the MCP spec, giving a uniform abstraction layer over arbitrarily different physical machines.
 
---
 
## ⚠️ Current Limitations
 
- LAN inference quality is bounded by the local server's hardware capabilities
- Cloud architecture introduces latency on each tool call
- Tool definitions (MCP drivers) must be manually authored per machine type
- No persistent memory between sessions
---
 
## 🚀 Roadmap Ideas
 
- Auto-generate MCP tool stubs from machine documentation
- Multi-agent coordination across multiple machines
- Real-time telemetry loop back into LLM context
- Web dashboard for monitoring active LARP deployments
---

## 📄 License

MIT License © 2026 Renganath Chokkalingam
Free to use, modify, and distribute with attribution.
