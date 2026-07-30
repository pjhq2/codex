from pathlib import Path
import os
import xlsxwriter


OUTPUT = Path(os.environ.get("MIPI_OUTPUT", "/Users/jhpark/work/codex/mipi_cts_ai.xlsx"))

MIPI_URL = "https://www.mipi.org/specifications/dsi"
TELEDYNE_URL = "https://cdn.teledynelecroy.com/files/pdf/envision_x84_datasheet.pdf"
SYNOPSYS_URL = "https://www.synopsys.com/verification/verification-ip/mipi/mipi-dsi.html"
AMD_URL = "https://docs.amd.com/r/en-US/pg238-mipi-dsi-tx/Verification-Compliance-and-Interoperability"


def item(test_id, dut, group, name, description, verify, applicability, priority, source):
    return {
        "id": test_id,
        "dut": dut,
        "group": group,
        "name": name,
        "description": description,
        "verify": verify,
        "applicability": applicability,
        "priority": priority,
        "source": source,
    }


tx = [
    item("AI-TX-PKT-01", "송신기 (Tx)", "1. 패킷 구조/식별", "Short Packet 헤더",
         "Short Packet의 Data ID, 2-byte data field와 ECC를 생성한다.",
         "Data Type·Virtual Channel·파라미터·ECC가 규정 형식으로 전송되는지 확인한다.",
         "공통", "P0", MIPI_URL),
    item("AI-TX-PKT-02", "송신기 (Tx)", "1. 패킷 구조/식별", "Long Packet 헤더/푸터",
         "Long Packet의 Word Count, payload, CRC를 포함한 packet boundary를 생성한다.",
         "Word Count와 실제 payload 길이가 일치하고 CRC 위치와 packet 종료가 정확한지 확인한다.",
         "공통", "P0", MIPI_URL),
    item("AI-TX-PKT-03", "송신기 (Tx)", "1. 패킷 구조/식별", "Data Type 인코딩",
         "명령·응답·비디오에 맞는 Data Type 값을 선택해 전송한다.",
         "지원 기능별 Data Type이 잘못 섞이거나 예약 값으로 전송되지 않는지 확인한다.",
         "공통", "P0", SYNOPSYS_URL),
    item("AI-TX-PKT-04", "송신기 (Tx)", "1. 패킷 구조/식별", "Virtual Channel 인코딩",
         "패킷의 Virtual Channel 식별자를 구성한다.",
         "선언된 VC 값이 모든 관련 패킷에서 일관되고 다른 논리 스트림과 혼선이 없는지 확인한다.",
         "복수 VC 지원 시", "P1", MIPI_URL),
    item("AI-TX-PKT-05", "송신기 (Tx)", "1. 패킷 구조/식별", "한 HS 구간 내 복수 패킷",
         "하나의 High-Speed 전송 구간에서 여러 패킷을 연속 배치한다.",
         "각 packet boundary와 패킷 순서가 유지되고 중간 바이트 유실·삽입이 없는지 확인한다.",
         "지원 시", "P1", SYNOPSYS_URL),
    item("AI-TX-PKT-06", "송신기 (Tx)", "1. 패킷 구조/식별", "End-of-Transmission Packet",
         "EoTp가 활성화된 구성에서 전송 종료 패킷을 생성한다.",
         "EoTp의 Data Type·내용·위치가 정확하고 다음 전송과 경계가 분명한지 확인한다.",
         "EoTp 사용 시", "P1", MIPI_URL),
    item("AI-TX-PKT-07", "송신기 (Tx)", "1. 패킷 구조/식별", "예약/미지원 Data Type 억제",
         "정상 동작 중 예약 또는 미지원 Data Type을 생성하지 않는다.",
         "설정 오류나 경계 조건에서도 불법 패킷이 링크로 출력되지 않는지 확인한다.",
         "공통", "P1", TELEDYNE_URL),

    item("AI-TX-ERR-01", "송신기 (Tx)", "2. 오류 보호", "Header ECC 생성",
         "모든 패킷 헤더에 대한 ECC를 계산한다.",
         "대표/경계 header 조합에서 계산된 ECC가 참조값과 일치하는지 확인한다.",
         "공통", "P0", SYNOPSYS_URL),
    item("AI-TX-ERR-02", "송신기 (Tx)", "2. 오류 보호", "Payload CRC 생성",
         "Long Packet payload에 대한 16-bit CRC를 생성한다.",
         "빈도 높은 길이와 최소·최대 지원 길이에서 CRC가 참조 계산과 일치하는지 확인한다.",
         "Long Packet", "P0", SYNOPSYS_URL),

    item("AI-TX-CMD-01", "송신기 (Tx)", "3. Command Mode", "Generic Short Write",
         "0/1/2 parameter Generic Short Write를 전송한다.",
         "parameter 수에 맞는 Data Type과 header data field가 선택되는지 확인한다.",
         "Command Mode 지원 시", "P0", MIPI_URL),
    item("AI-TX-CMD-02", "송신기 (Tx)", "3. Command Mode", "Generic Long Write",
         "가변 길이 Generic Long Write payload를 전송한다.",
         "Word Count·payload 순서·CRC가 정확하고 길이 경계에서 잘리지 않는지 확인한다.",
         "Command Mode 지원 시", "P0", MIPI_URL),
    item("AI-TX-CMD-03", "송신기 (Tx)", "3. Command Mode", "Generic Read Request",
         "0/1/2 parameter Generic Read Request를 전송한다.",
         "요청 길이에 맞는 Data Type, 파라미터 및 뒤따르는 BTA가 정확한지 확인한다.",
         "Read 지원 시", "P0", MIPI_URL),
    item("AI-TX-CMD-04", "송신기 (Tx)", "3. Command Mode", "DCS Short Write",
         "0/1 parameter DCS Short Write를 전송한다.",
         "DCS command와 parameter가 올바른 short packet 형식으로 전달되는지 확인한다.",
         "DCS 지원 시", "P0", MIPI_URL),
    item("AI-TX-CMD-05", "송신기 (Tx)", "3. Command Mode", "DCS Long Write",
         "여러 parameter를 포함하는 DCS Long Write를 전송한다.",
         "command byte가 payload 선두에 있고 Word Count·CRC·payload 순서가 정확한지 확인한다.",
         "DCS 지원 시", "P0", MIPI_URL),
    item("AI-TX-CMD-06", "송신기 (Tx)", "3. Command Mode", "DCS Read Request",
         "DCS Read Request와 응답 수신 절차를 시작한다.",
         "request packet, BTA 요청, 응답 대기 순서가 올바른지 확인한다.",
         "DCS Read 지원 시", "P0", MIPI_URL),
    item("AI-TX-CMD-07", "송신기 (Tx)", "3. Command Mode", "Set Maximum Return Packet Size",
         "수신 가능한 최대 return packet 크기를 상대 장치에 알린다.",
         "설정값이 정확히 인코딩되고 후속 read response 길이 제한과 일치하는지 확인한다.",
         "Read 지원 시", "P1", MIPI_URL),
    item("AI-TX-CMD-08", "송신기 (Tx)", "3. Command Mode", "Peripheral 제어 패킷",
         "Shutdown, Turn On, Color Mode 등 지원하는 제어 패킷을 전송한다.",
         "선택한 제어 명령의 Data Type과 parameter가 의도한 상태 전환을 일으키는지 확인한다.",
         "해당 명령 지원 시", "P1", MIPI_URL),
    item("AI-TX-CMD-09", "송신기 (Tx)", "3. Command Mode", "Command Mode Pixel Write",
         "Memory Write 계열 DCS 명령으로 화면 픽셀 데이터를 전송한다.",
         "주소 설정 이후 pixel payload의 시작·계속 전송·종료가 올바른지 확인한다.",
         "Command Mode Display", "P1", AMD_URL),

    item("AI-TX-BTA-01", "송신기 (Tx)", "4. BTA/응답", "Bus Turn-Around 요청",
         "읽기 또는 ACK 수신을 위해 버스 방향 전환을 요청한다.",
         "요청 시점과 lane ownership 전환이 정확하며 양쪽이 동시에 구동하지 않는지 확인한다.",
         "Read/BTA 지원 시", "P0", MIPI_URL),
    item("AI-TX-BTA-02", "송신기 (Tx)", "4. BTA/응답", "응답 대기 윈도우",
         "BTA 후 상대 장치의 short/long response를 기다린다.",
         "응답 시작 전 버스를 재점유하지 않고 timeout 조건을 올바르게 처리하는지 확인한다.",
         "Read/BTA 지원 시", "P1", TELEDYNE_URL),
    item("AI-TX-BTA-03", "송신기 (Tx)", "4. BTA/응답", "ACK and Error Report 수신",
         "상대 장치가 반환한 Acknowledge and Error Report를 해석한다.",
         "오류 비트가 원인별로 식별되어 상위 로직에 전달되고 정상 응답과 구분되는지 확인한다.",
         "ACK/Error Report 지원 시", "P1", MIPI_URL),
    item("AI-TX-BTA-04", "송신기 (Tx)", "4. BTA/응답", "Short/Long Read Response 수신",
         "Generic/DCS short 및 long read response를 수신한다.",
         "응답 Data Type·길이·CRC와 요청 간 대응이 정확한지 확인한다.",
         "Read 지원 시", "P1", MIPI_URL),

    item("AI-TX-VID-01", "송신기 (Tx)", "5. Video Mode/타이밍", "Non-Burst with Sync Pulses",
         "HSS/HSE와 blanking 구간을 포함한 non-burst sync-pulse video를 전송한다.",
         "HSA·HBP·active·HFP 구간과 line time이 설정값에 맞는지 확인한다.",
         "해당 Video Mode 지원 시", "P0", TELEDYNE_URL),
    item("AI-TX-VID-02", "송신기 (Tx)", "5. Video Mode/타이밍", "Non-Burst with Sync Events",
         "sync event 기반 non-burst video stream을 전송한다.",
         "HSS 중심의 line sequence와 active/blanking 배치가 규정 순서인지 확인한다.",
         "해당 Video Mode 지원 시", "P0", TELEDYNE_URL),
    item("AI-TX-VID-03", "송신기 (Tx)", "5. Video Mode/타이밍", "Burst Mode",
         "active pixel을 burst로 보내고 나머지 line time을 blanking으로 유지한다.",
         "burst 길이·전송률·line time과 blanking 시간이 설정값에 맞는지 확인한다.",
         "Burst Mode 지원 시", "P0", TELEDYNE_URL),
    item("AI-TX-VID-04", "송신기 (Tx)", "5. Video Mode/타이밍", "수직 동기 시퀀스",
         "VSS/VSE 및 vertical back/front porch line sequence를 생성한다.",
         "프레임당 line 수와 VSA/VBP/VFP/active line 순서가 정확한지 확인한다.",
         "Video Mode 지원 시", "P0", TELEDYNE_URL),
    item("AI-TX-VID-05", "송신기 (Tx)", "5. Video Mode/타이밍", "수평 동기 시퀀스",
         "각 line의 HSS/HSE와 horizontal blanking을 생성한다.",
         "모든 line에서 동기 event 누락·중복이 없고 active pixel 위치가 일정한지 확인한다.",
         "Video Mode 지원 시", "P0", TELEDYNE_URL),
    item("AI-TX-VID-06", "송신기 (Tx)", "5. Video Mode/타이밍", "Blanking/Porch 구성",
         "H/V blanking과 front/back porch에 필요한 packet 또는 idle 시간을 배치한다.",
         "최소 timing, line/frame 총 길이 및 상대 장치 요구사항을 만족하는지 확인한다.",
         "Video Mode 지원 시", "P1", TELEDYNE_URL),
    item("AI-TX-VID-07", "송신기 (Tx)", "5. Video Mode/타이밍", "Null Packet/Blanking Packet",
         "필요한 경우 남는 전송 시간을 Null Packet 등으로 채운다.",
         "Word Count와 CRC가 정확하고 active video로 오인되지 않는지 확인한다.",
         "사용 시", "P1", TELEDYNE_URL),
    item("AI-TX-VID-08", "송신기 (Tx)", "5. Video Mode/타이밍", "연속 프레임 안정성",
         "여러 프레임을 연속 전송하며 packet/timing 일관성을 유지한다.",
         "frame boundary, frame rate, 누락·중복 line과 장시간 drift가 없는지 확인한다.",
         "Video Mode 지원 시", "P1", AMD_URL),

    item("AI-TX-PIX-01", "송신기 (Tx)", "6. 픽셀 포맷/멀티 Lane", "RGB565 전송",
         "16-bit RGB565 pixel stream을 패킹해 전송한다.",
         "색상 성분 bit 위치, pixel 순서, line payload 길이가 기준 영상과 일치하는지 확인한다.",
         "RGB565 지원 시", "P1", SYNOPSYS_URL),
    item("AI-TX-PIX-02", "송신기 (Tx)", "6. 픽셀 포맷/멀티 Lane", "RGB666 Loosely Packed",
         "18-bit RGB666을 loosely packed 형식으로 전송한다.",
         "padding bit와 성분 정렬, pixel 순서 및 Word Count가 정확한지 확인한다.",
         "RGB666 Loose 지원 시", "P1", SYNOPSYS_URL),
    item("AI-TX-PIX-03", "송신기 (Tx)", "6. 픽셀 포맷/멀티 Lane", "RGB666 Packed",
         "18-bit RGB666을 packed 형식으로 전송한다.",
         "4-pixel 단위 packing 경계와 line 끝 정렬이 정확한지 확인한다.",
         "RGB666 Packed 지원 시", "P1", SYNOPSYS_URL),
    item("AI-TX-PIX-04", "송신기 (Tx)", "6. 픽셀 포맷/멀티 Lane", "RGB888 전송",
         "24-bit RGB888 pixel stream을 전송한다.",
         "R/G/B byte 순서, pixel 순서와 line payload 길이가 기준 영상과 일치하는지 확인한다.",
         "RGB888 지원 시", "P0", SYNOPSYS_URL),
    item("AI-TX-PIX-05", "송신기 (Tx)", "6. 픽셀 포맷/멀티 Lane", "멀티 Lane Byte 분배",
         "packet byte stream을 활성 data lane 수에 맞게 분배한다.",
         "lane별 byte 순서, 첫/마지막 byte 위치와 재조합 결과가 원 packet과 같은지 확인한다.",
         "2개 이상 Lane 지원 시", "P0", AMD_URL),
    item("AI-TX-PIX-06", "송신기 (Tx)", "6. 픽셀 포맷/멀티 Lane", "Line 끝 Padding/정렬",
         "pixel packing 또는 lane 분배로 필요한 line 끝 정렬을 처리한다.",
         "불필요한 pixel이 표시되지 않고 Word Count 및 다음 packet 시작이 정확한지 확인한다.",
         "포맷/해상도 의존", "P1", TELEDYNE_URL),

    item("AI-TX-CMP-01", "송신기 (Tx)", "7. 압축(선택)", "DSC/PPS 설정 전송",
         "지원 시 압축 스트림에 필요한 설정 또는 PPS 정보를 전송한다.",
         "encoder 설정과 display decoder 설정이 일치하고 frame 적용 시점이 정확한지 확인한다.",
         "DSC 지원 시", "P2", MIPI_URL),
    item("AI-TX-CMP-02", "송신기 (Tx)", "7. 압축(선택)", "Compressed Pixel Stream",
         "압축된 pixel stream을 정의된 packetization으로 전송한다.",
         "slice/chunk 경계, Word Count, CRC와 복원 영상의 무결성을 확인한다.",
         "DSC 지원 시", "P2", MIPI_URL),

    item("AI-TX-PWR-01", "송신기 (Tx)", "8. LP/HS/전력 상태", "LPDT/Escape 전송",
         "Escape entry 후 Low-Power Data Transmission을 수행한다.",
         "entry sequence, bit encoding, payload와 exit가 정확하고 상대 장치가 해석하는지 확인한다.",
         "LPDT 지원 시", "P0", TELEDYNE_URL),
    item("AI-TX-PWR-02", "송신기 (Tx)", "8. LP/HS/전력 상태", "HS 전송 진입/종료",
         "LP 상태에서 High-Speed 전송을 시작하고 다시 LP 상태로 복귀한다.",
         "전환 순서, 첫/마지막 protocol byte와 packet 경계가 손상되지 않는지 확인한다.",
         "공통", "P0", TELEDYNE_URL),
    item("AI-TX-PWR-03", "송신기 (Tx)", "8. LP/HS/전력 상태", "Command/Video 전환",
         "지원되는 구성에서 command traffic과 video traffic 사이를 전환한다.",
         "전환 중 미완료 packet, frame 손상 또는 잘못된 BTA가 발생하지 않는지 확인한다.",
         "두 Mode 모두 지원 시", "P1", SYNOPSYS_URL),
    item("AI-TX-PWR-04", "송신기 (Tx)", "8. LP/HS/전력 상태", "ULPS 진입/복귀",
         "Ultra Low Power State로 진입한 뒤 정상 통신 상태로 복귀한다.",
         "진입·복귀 시퀀스와 복귀 후 첫 packet이 정상 수신되는지 확인한다.",
         "ULPS 지원 시", "P1", MIPI_URL),
    item("AI-TX-PWR-05", "송신기 (Tx)", "8. LP/HS/전력 상태", "Timeout/복구",
         "응답 부재나 비정상 전환 후 송신 상태 머신을 복구한다.",
         "버스 고착 없이 규정된 timeout 처리를 수행하고 다음 정상 transaction이 가능한지 확인한다.",
         "오류 복구 지원 시", "P1", AMD_URL),
]


rx = [
    item("AI-RX-PKT-01", "수신기 (Rx)", "1. 패킷 수신/식별", "Short Packet 파싱",
         "Short Packet header와 data field를 수신·해석한다.",
         "Data Type·VC·파라미터가 정확히 복원되어 올바른 내부 기능으로 전달되는지 확인한다.",
         "공통", "P0", MIPI_URL),
    item("AI-RX-PKT-02", "수신기 (Rx)", "1. 패킷 수신/식별", "Long Packet 파싱",
         "Word Count만큼 payload를 수신하고 CRC 및 packet 종료를 해석한다.",
         "payload 경계, 첫/마지막 byte와 다음 packet 시작을 정확히 구분하는지 확인한다.",
         "공통", "P0", MIPI_URL),
    item("AI-RX-PKT-03", "수신기 (Rx)", "1. 패킷 수신/식별", "Data Type 디코딩",
         "수신 Data Type에 따라 command, response, pixel data를 분류한다.",
         "지원하는 모든 Data Type이 올바른 처리 경로로 전달되는지 확인한다.",
         "공통", "P0", SYNOPSYS_URL),
    item("AI-RX-PKT-04", "수신기 (Rx)", "1. 패킷 수신/식별", "Virtual Channel 분리",
         "Virtual Channel별 패킷을 식별하고 대상 context로 전달한다.",
         "VC 간 데이터 혼합·오인식이 없고 미지원 VC의 처리 정책이 일관적인지 확인한다.",
         "복수 VC 지원 시", "P1", MIPI_URL),
    item("AI-RX-PKT-05", "수신기 (Rx)", "1. 패킷 수신/식별", "한 HS 구간 내 복수 패킷",
         "하나의 HS 구간에 연속된 여러 패킷을 수신한다.",
         "각 packet boundary를 유지하고 모든 패킷을 순서대로 전달하는지 확인한다.",
         "지원 시", "P1", SYNOPSYS_URL),
    item("AI-RX-PKT-06", "수신기 (Rx)", "1. 패킷 수신/식별", "EoTp 수신",
         "End-of-Transmission Packet을 인식한다.",
         "EoTp가 payload로 전달되지 않고 전송 종료 및 다음 상태 전이에 올바르게 반영되는지 확인한다.",
         "EoTp 사용 시", "P1", MIPI_URL),
    item("AI-RX-PKT-07", "수신기 (Rx)", "1. 패킷 수신/식별", "예약/미지원 Data Type 처리",
         "예약 또는 미지원 Data Type 수신 시 안전하게 처리한다.",
         "정상 데이터로 오인하지 않고 drop·ignore·오류 보고 중 선언한 정책을 수행하는지 확인한다.",
         "공통", "P1", TELEDYNE_URL),

    item("AI-RX-ERR-01", "수신기 (Rx)", "2. 오류 검출/보고", "ECC 단일 비트 정정",
         "header에 단일 비트 오류가 있는 패킷을 수신한다.",
         "정정 가능한 오류를 올바르게 정정하고 packet 처리와 오류 상태를 규정대로 유지하는지 확인한다.",
         "공통", "P0", SYNOPSYS_URL),
    item("AI-RX-ERR-02", "수신기 (Rx)", "2. 오류 검출/보고", "ECC 복수 비트 검출",
         "정정 불가능한 header 오류를 포함한 패킷을 수신한다.",
         "오류 패킷을 정상 수용하지 않고 검출·폐기·보고 정책을 수행하는지 확인한다.",
         "공통", "P0", SYNOPSYS_URL),
    item("AI-RX-ERR-03", "수신기 (Rx)", "2. 오류 검출/보고", "CRC 오류 검출",
         "payload 또는 CRC가 손상된 Long Packet을 수신한다.",
         "CRC mismatch를 검출하고 손상 payload가 표시/명령 처리에 사용되지 않는지 확인한다.",
         "Long Packet", "P0", SYNOPSYS_URL),
    item("AI-RX-ERR-04", "수신기 (Rx)", "2. 오류 검출/보고", "Word Count 불일치",
         "선언된 Word Count와 실제 payload 길이가 다른 패킷을 수신한다.",
         "underflow/overflow를 검출하고 다음 packet boundary를 안전하게 회복하는지 확인한다.",
         "공통", "P0", TELEDYNE_URL),
    item("AI-RX-ERR-05", "수신기 (Rx)", "2. 오류 검출/보고", "잘못된 Packet Sequence",
         "video event 또는 command sequence 순서가 잘못된 스트림을 수신한다.",
         "상태 머신이 오류를 검출하고 이후 정상 frame/transaction으로 복구하는지 확인한다.",
         "공통", "P1", TELEDYNE_URL),
    item("AI-RX-ERR-06", "수신기 (Rx)", "2. 오류 검출/보고", "수신 Timeout",
         "불완전한 packet 또는 중단된 turnaround를 입력한다.",
         "무한 대기 없이 timeout을 발생시키고 lane/프로토콜 상태를 복구하는지 확인한다.",
         "공통", "P1", AMD_URL),
    item("AI-RX-ERR-07", "수신기 (Rx)", "2. 오류 검출/보고", "ACK and Error Report 생성",
         "검출된 오류를 Acknowledge and Error Report로 반환한다.",
         "오류 원인에 대응하는 bit가 정확하고 BTA response packet 형식이 올바른지 확인한다.",
         "Error Report 지원 시", "P1", MIPI_URL),
    item("AI-RX-ERR-08", "수신기 (Rx)", "2. 오류 검출/보고", "오류 후 정상 트래픽 복구",
         "오류 패킷 뒤에 유효한 packet/frame을 연속 입력한다.",
         "오류가 다음 정상 transaction으로 전파되지 않고 정상 수신을 재개하는지 확인한다.",
         "공통", "P1", AMD_URL),

    item("AI-RX-CMD-01", "수신기 (Rx)", "3. Command Mode/응답", "Generic Short Write 수신",
         "0/1/2 parameter Generic Short Write를 수신한다.",
         "parameter 수별 Data Type과 값이 정확히 전달되고 잘못된 길이는 거부되는지 확인한다.",
         "Command Mode 지원 시", "P0", MIPI_URL),
    item("AI-RX-CMD-02", "수신기 (Rx)", "3. Command Mode/응답", "Generic Long Write 수신",
         "가변 길이 Generic Long Write를 수신한다.",
         "Word Count·payload·CRC 검증 후 전체 데이터가 순서대로 내부 로직에 전달되는지 확인한다.",
         "Command Mode 지원 시", "P0", MIPI_URL),
    item("AI-RX-CMD-03", "수신기 (Rx)", "3. Command Mode/응답", "Generic Read Request 처리",
         "0/1/2 parameter Generic Read Request를 처리한다.",
         "요청에 대응하는 register/data를 선택하고 올바른 response 형태를 생성하는지 확인한다.",
         "Read 지원 시", "P0", MIPI_URL),
    item("AI-RX-CMD-04", "수신기 (Rx)", "3. Command Mode/응답", "DCS Short Write 수신",
         "0/1 parameter DCS Short Write를 수신한다.",
         "명령 및 parameter가 DCS 처리부에 정확히 전달되고 상태 변화가 의도와 같은지 확인한다.",
         "DCS 지원 시", "P0", MIPI_URL),
    item("AI-RX-CMD-05", "수신기 (Rx)", "3. Command Mode/응답", "DCS Long Write 수신",
         "여러 parameter의 DCS Long Write를 수신한다.",
         "command byte·payload 길이·CRC를 검증하고 원자적으로 적용하는지 확인한다.",
         "DCS 지원 시", "P0", MIPI_URL),
    item("AI-RX-CMD-06", "수신기 (Rx)", "3. Command Mode/응답", "DCS Read Request 처리",
         "DCS Read Request에 맞는 상태/레지스터 데이터를 준비한다.",
         "지원/미지원 command를 구분하고 BTA 후 정확한 response를 생성하는지 확인한다.",
         "DCS Read 지원 시", "P0", MIPI_URL),
    item("AI-RX-CMD-07", "수신기 (Rx)", "3. Command Mode/응답", "Maximum Return Size 준수",
         "Host가 설정한 Maximum Return Packet Size를 저장·적용한다.",
         "응답 payload가 제한을 넘지 않고 필요한 경우 적절한 길이로 반환되는지 확인한다.",
         "Read 지원 시", "P1", MIPI_URL),
    item("AI-RX-CMD-08", "수신기 (Rx)", "3. Command Mode/응답", "Short Read Response 생성",
         "1-byte 또는 2-byte Generic/DCS short response를 생성한다.",
         "응답 종류·Data Type·data field·ECC가 요청 및 데이터 길이와 일치하는지 확인한다.",
         "Read 지원 시", "P0", MIPI_URL),
    item("AI-RX-CMD-09", "수신기 (Rx)", "3. Command Mode/응답", "Long Read Response 생성",
         "2 byte를 넘는 Generic/DCS long response를 생성한다.",
         "Word Count·payload·CRC와 Maximum Return Size 준수가 정확한지 확인한다.",
         "Long Read 지원 시", "P0", MIPI_URL),
    item("AI-RX-CMD-10", "수신기 (Rx)", "3. Command Mode/응답", "Command Mode Pixel Write",
         "Memory Write 계열 DCS payload를 frame memory에 반영한다.",
         "주소 window, pixel order, continue write와 마지막 pixel 처리가 정확한지 확인한다.",
         "Command Mode Display", "P1", AMD_URL),
    item("AI-RX-CMD-11", "수신기 (Rx)", "3. Command Mode/응답", "Peripheral 제어 명령",
         "Shutdown, Turn On, Color Mode 등 지원 명령을 처리한다.",
         "명령별 상태 전환과 ACK/오류 처리 및 이후 통신 가능 여부를 확인한다.",
         "해당 명령 지원 시", "P1", MIPI_URL),
    item("AI-RX-CMD-12", "수신기 (Rx)", "3. Command Mode/응답", "미지원 명령 처리",
         "미지원 또는 잘못 구성된 command packet을 입력한다.",
         "오동작 없이 무시하거나 오류를 보고하고 기존 display 상태를 보존하는지 확인한다.",
         "공통", "P1", TELEDYNE_URL),

    item("AI-RX-BTA-01", "수신기 (Rx)", "4. BTA/버스 소유권", "BTA 감지/소유권 획득",
         "Host의 BTA 요청 후 response transmitter로 전환한다.",
         "lane contention 없이 정해진 순서로 버스 소유권을 획득하는지 확인한다.",
         "Read/BTA 지원 시", "P0", MIPI_URL),
    item("AI-RX-BTA-02", "수신기 (Rx)", "4. BTA/버스 소유권", "응답 시작 Timing",
         "BTA 이후 ACK 또는 read response 전송을 시작한다.",
         "응답 지연이 허용 범위에 있고 Host timeout 전에 시작되는지 확인한다.",
         "Read/BTA 지원 시", "P1", TELEDYNE_URL),
    item("AI-RX-BTA-03", "수신기 (Rx)", "4. BTA/버스 소유권", "Response 종료/반환",
         "response를 끝내고 버스 소유권을 Host로 반환한다.",
         "마지막 byte와 LP state 전환이 정확하고 다음 Host transaction을 방해하지 않는지 확인한다.",
         "Read/BTA 지원 시", "P0", MIPI_URL),
    item("AI-RX-BTA-04", "수신기 (Rx)", "4. BTA/버스 소유권", "비정상 BTA 복구",
         "중단되거나 잘못된 turnaround sequence를 입력한다.",
         "동시 구동이나 고착 없이 timeout 후 정상 receive mode로 복귀하는지 확인한다.",
         "오류 복구 지원 시", "P1", AMD_URL),

    item("AI-RX-VID-01", "수신기 (Rx)", "5. Video Mode/타이밍", "Non-Burst Sync Pulses 수신",
         "sync pulse 방식의 non-burst video stream을 수신한다.",
         "HSA/HBP/active/HFP와 line boundary를 올바르게 해석하는지 확인한다.",
         "해당 Video Mode 지원 시", "P0", TELEDYNE_URL),
    item("AI-RX-VID-02", "수신기 (Rx)", "5. Video Mode/타이밍", "Non-Burst Sync Events 수신",
         "sync event 방식의 non-burst video stream을 수신한다.",
         "HSS event, blanking과 active pixel 위치를 정확히 복원하는지 확인한다.",
         "해당 Video Mode 지원 시", "P0", TELEDYNE_URL),
    item("AI-RX-VID-03", "수신기 (Rx)", "5. Video Mode/타이밍", "Burst Mode 수신",
         "active pixel burst와 긴 blanking 구간을 수신한다.",
         "burst 종료 후 line timing을 유지하고 다음 line/frame을 정상 인식하는지 확인한다.",
         "Burst Mode 지원 시", "P0", TELEDYNE_URL),
    item("AI-RX-VID-04", "수신기 (Rx)", "5. Video Mode/타이밍", "수직 동기/Frame Boundary",
         "VSS/VSE와 vertical porch를 이용해 frame boundary를 구성한다.",
         "프레임 line 수, active 영역 시작·끝과 frame rate가 설정값과 일치하는지 확인한다.",
         "Video Mode 지원 시", "P0", TELEDYNE_URL),
    item("AI-RX-VID-05", "수신기 (Rx)", "5. Video Mode/타이밍", "수평 동기/Line Boundary",
         "HSS/HSE 및 line packet sequence를 해석한다.",
         "누락·중복 line 없이 active pixel이 올바른 line 위치에 기록되는지 확인한다.",
         "Video Mode 지원 시", "P0", TELEDYNE_URL),
    item("AI-RX-VID-06", "수신기 (Rx)", "5. Video Mode/타이밍", "Blanking/Null Packet 처리",
         "blanking interval과 Null Packet을 비표시 데이터로 처리한다.",
         "blanking payload가 화면에 나타나지 않고 line/frame timing만 유지되는지 확인한다.",
         "Video Mode 지원 시", "P1", TELEDYNE_URL),
    item("AI-RX-VID-07", "수신기 (Rx)", "5. Video Mode/타이밍", "연속 프레임 안정성",
         "동일하거나 변화하는 영상을 여러 프레임 연속 수신한다.",
         "frame drop·repeat·tear, line drift와 장시간 상태 누적 오류가 없는지 확인한다.",
         "Video Mode 지원 시", "P1", AMD_URL),

    item("AI-RX-PIX-01", "수신기 (Rx)", "6. 픽셀 포맷/멀티 Lane", "RGB565 Unpack",
         "RGB565 pixel payload를 unpack해 표시 경로로 전달한다.",
         "성분 bit 위치와 pixel 순서가 golden image와 일치하는지 확인한다.",
         "RGB565 지원 시", "P1", SYNOPSYS_URL),
    item("AI-RX-PIX-02", "수신기 (Rx)", "6. 픽셀 포맷/멀티 Lane", "RGB666 Loosely Packed Unpack",
         "loosely packed RGB666을 18-bit pixel로 복원한다.",
         "padding bit 처리, 색상 성분과 line 끝 정렬이 정확한지 확인한다.",
         "RGB666 Loose 지원 시", "P1", SYNOPSYS_URL),
    item("AI-RX-PIX-03", "수신기 (Rx)", "6. 픽셀 포맷/멀티 Lane", "RGB666 Packed Unpack",
         "packed RGB666 byte stream을 pixel로 복원한다.",
         "4-pixel packing 경계와 line 끝의 부분 그룹 처리가 정확한지 확인한다.",
         "RGB666 Packed 지원 시", "P1", SYNOPSYS_URL),
    item("AI-RX-PIX-04", "수신기 (Rx)", "6. 픽셀 포맷/멀티 Lane", "RGB888 Unpack",
         "RGB888 byte stream을 24-bit pixel로 복원한다.",
         "R/G/B byte 순서, pixel 순서와 line stride가 golden image와 일치하는지 확인한다.",
         "RGB888 지원 시", "P0", SYNOPSYS_URL),
    item("AI-RX-PIX-05", "수신기 (Rx)", "6. 픽셀 포맷/멀티 Lane", "멀티 Lane Byte 재조합",
         "여러 data lane의 byte stream을 원래 packet 순서로 재조합한다.",
         "lane별 첫 byte, round-robin 순서와 packet 끝에서 유실·중복이 없는지 확인한다.",
         "2개 이상 Lane 지원 시", "P0", AMD_URL),
    item("AI-RX-PIX-06", "수신기 (Rx)", "6. 픽셀 포맷/멀티 Lane", "Padding/Line 끝 처리",
         "pixel packing과 lane 분배에 따른 line 끝 정렬을 처리한다.",
         "padding을 pixel로 표시하지 않고 다음 line 첫 pixel이 정확한지 확인한다.",
         "포맷/해상도 의존", "P1", TELEDYNE_URL),

    item("AI-RX-CMP-01", "수신기 (Rx)", "7. 압축(선택)", "DSC/PPS 적용",
         "수신한 압축 설정 또는 PPS를 decoder 구성에 반영한다.",
         "설정값, 적용 frame과 encoder/decoder 조합이 일치하는지 확인한다.",
         "DSC 지원 시", "P2", MIPI_URL),
    item("AI-RX-CMP-02", "수신기 (Rx)", "7. 압축(선택)", "Compressed Pixel Stream 복원",
         "압축된 pixel payload를 수신해 복원한다.",
         "slice/chunk boundary, 오류 처리와 복원 영상의 무결성을 확인한다.",
         "DSC 지원 시", "P2", MIPI_URL),

    item("AI-RX-PWR-01", "수신기 (Rx)", "8. LP/HS/전력 상태", "LPDT/Escape 수신",
         "Escape sequence와 Low-Power Data Transmission을 수신한다.",
         "entry, bit decoding, payload와 exit를 정확히 인식하고 명령 경로로 전달하는지 확인한다.",
         "LPDT 지원 시", "P0", TELEDYNE_URL),
    item("AI-RX-PWR-02", "수신기 (Rx)", "8. LP/HS/전력 상태", "HS 진입/종료 인식",
         "상대 장치의 High-Speed 전송 시작과 종료를 인식한다.",
         "첫 protocol byte부터 마지막 byte까지 누락 없이 capture하고 LP 상태로 복귀하는지 확인한다.",
         "공통", "P0", TELEDYNE_URL),
    item("AI-RX-PWR-03", "수신기 (Rx)", "8. LP/HS/전력 상태", "Command/Video 전환 수용",
         "command traffic과 video traffic의 전환을 수용한다.",
         "전환 중 기존 frame/command 상태를 안전하게 마감하고 새 mode를 정상 처리하는지 확인한다.",
         "두 Mode 모두 지원 시", "P1", SYNOPSYS_URL),
    item("AI-RX-PWR-04", "수신기 (Rx)", "8. LP/HS/전력 상태", "ULPS 진입/복귀 수용",
         "Ultra Low Power State 요청을 수용하고 exit 후 수신을 재개한다.",
         "ULPS 동안 잘못된 처리 없이 유지되고 exit 후 첫 packet을 정상 수신하는지 확인한다.",
         "ULPS 지원 시", "P1", MIPI_URL),
    item("AI-RX-PWR-05", "수신기 (Rx)", "8. LP/HS/전력 상태", "비정상 전환 복구",
         "불완전한 LP/HS 전환 또는 중단된 transmission을 입력한다.",
         "상태 고착 없이 timeout·오류 처리 후 다음 정상 transmission을 수신하는지 확인한다.",
         "오류 복구 지원 시", "P1", AMD_URL),
]


all_items = tx + rx
last_checklist_row = 4 + len(all_items)


workbook = xlsxwriter.Workbook(
    OUTPUT,
    {
        "constant_memory": False,
        "strings_to_urls": True,
    },
)
workbook.set_properties(
    {
        "title": "MIPI DSI v1.3.1 CTS 공개 범위 기반 테스트 체크리스트",
        "subject": "MIPI DSI v1.3.1 Transmitter/Receiver Protocol CTS 요약",
        "author": "OpenAI Codex",
        "company": "",
        "comments": "공식 CTS 원문의 Test ID, 절차 및 판정 기준을 대체하지 않는 공개 근거 기반 실무 체크리스트",
    }
)


COLORS = {
    "navy": "#17365D",
    "blue": "#1F4E78",
    "light_blue": "#D9EAF7",
    "teal": "#0F6B78",
    "light_teal": "#DDEBF7",
    "green": "#548235",
    "light_green": "#E2F0D9",
    "amber": "#BF9000",
    "light_amber": "#FFF2CC",
    "red": "#C00000",
    "light_red": "#FCE4D6",
    "purple": "#7030A0",
    "light_purple": "#E4DFEC",
    "gray": "#666666",
    "light_gray": "#F2F2F2",
    "border": "#C9D4E1",
    "white": "#FFFFFF",
    "black": "#1F2937",
}

group_colors = {
    "1. 패킷 구조/식별": COLORS["light_blue"],
    "1. 패킷 수신/식별": COLORS["light_blue"],
    "2. 오류 보호": COLORS["light_red"],
    "2. 오류 검출/보고": COLORS["light_red"],
    "3. Command Mode": COLORS["light_purple"],
    "3. Command Mode/응답": COLORS["light_purple"],
    "4. BTA/응답": COLORS["light_amber"],
    "4. BTA/버스 소유권": COLORS["light_amber"],
    "5. Video Mode/타이밍": COLORS["light_green"],
    "6. 픽셀 포맷/멀티 Lane": COLORS["light_teal"],
    "7. 압축(선택)": "#FCE4D6",
    "8. LP/HS/전력 상태": "#FFF2CC",
}


def fmt(props):
    base = {"font_name": "Apple SD Gothic Neo", "font_size": 9, "font_color": COLORS["black"]}
    base.update(props)
    return workbook.add_format(base)


title_fmt = fmt(
    {
        "bold": True,
        "font_size": 17,
        "font_color": COLORS["white"],
        "bg_color": COLORS["navy"],
        "align": "center",
        "valign": "vcenter",
    }
)
subtitle_fmt = fmt(
    {
        "italic": True,
        "font_size": 9,
        "font_color": "#334155",
        "bg_color": "#EAF2F8",
        "text_wrap": True,
        "valign": "vcenter",
        "border": 1,
        "border_color": COLORS["border"],
    }
)
header_fmt = fmt(
    {
        "bold": True,
        "font_color": COLORS["white"],
        "bg_color": COLORS["blue"],
        "align": "center",
        "valign": "vcenter",
        "text_wrap": True,
        "border": 1,
        "border_color": COLORS["white"],
    }
)
body_fmt = fmt(
    {
        "text_wrap": True,
        "valign": "top",
        "border": 1,
        "border_color": "#E1E7EF",
    }
)
body_center_fmt = fmt(
    {
        "align": "center",
        "valign": "vcenter",
        "text_wrap": True,
        "border": 1,
        "border_color": "#E1E7EF",
    }
)
source_fmt = fmt(
    {
        "font_color": "#0563C1",
        "underline": True,
        "text_wrap": True,
        "valign": "top",
        "border": 1,
        "border_color": "#E1E7EF",
    }
)
note_fmt = fmt(
    {
        "bg_color": COLORS["light_amber"],
        "font_color": "#7F6000",
        "italic": True,
        "text_wrap": True,
        "valign": "vcenter",
        "border": 1,
        "border_color": "#E6D58A",
    }
)
section_fmt = fmt(
    {
        "bold": True,
        "font_size": 11,
        "font_color": COLORS["white"],
        "bg_color": COLORS["teal"],
        "align": "left",
        "valign": "vcenter",
    }
)
card_label_fmt = fmt(
    {
        "bold": True,
        "font_color": "#44546A",
        "bg_color": COLORS["light_gray"],
        "align": "center",
        "valign": "vcenter",
        "border": 1,
        "border_color": COLORS["border"],
    }
)
card_value_fmt = fmt(
    {
        "bold": True,
        "font_size": 18,
        "font_color": COLORS["blue"],
        "bg_color": COLORS["white"],
        "align": "center",
        "valign": "vcenter",
        "border": 1,
        "border_color": COLORS["border"],
        "num_format": "#,##0",
    }
)
percent_fmt = fmt(
    {
        "bold": True,
        "font_size": 18,
        "font_color": COLORS["green"],
        "bg_color": COLORS["white"],
        "align": "center",
        "valign": "vcenter",
        "border": 1,
        "border_color": COLORS["border"],
        "num_format": "0%",
    }
)


def configure_sheet(ws, tab_color):
    ws.hide_gridlines(2)
    ws.set_tab_color(tab_color)
    ws.set_default_row(18)
    ws.freeze_panes(4, 0)
    ws.set_landscape()
    ws.set_paper(8)
    ws.fit_to_pages(1, 0)
    ws.set_margins(0.25, 0.25, 0.35, 0.35)
    ws.repeat_rows(3)
    ws.set_header("&C&\"Apple SD Gothic Neo,Bold\"MIPI DSI v1.3.1 CTS 요약")
    ws.set_footer("&L공개 범위 기반 체크리스트&RPage &P of &N")


def group_format(group, center=False, top=False):
    props = {
        "bg_color": group_colors[group],
        "bold": center,
        "align": "center" if center else "left",
        "valign": "vcenter" if center else "top",
        "text_wrap": True,
        "border": 1,
        "border_color": "#E1E7EF",
    }
    if top:
        props["top"] = 2
        props["top_color"] = COLORS["blue"]
    return fmt(props)


def add_detail_sheet(name, title, direction_note, data, tab_color):
    ws = workbook.add_worksheet(name)
    configure_sheet(ws, tab_color)
    ws.merge_range("A1:H1", title, title_fmt)
    ws.set_row(0, 31)
    ws.merge_range("A2:H2", direction_note, subtitle_fmt)
    ws.set_row(1, 48)
    ws.merge_range(
        "A3:H3",
        "내부 ID는 공식 MIPI Test ID가 아닙니다. 적용 조건이 있는 행은 DUT capability 선언 및 회원용 CTS 원문으로 최종 적용 여부를 확인하세요.",
        note_fmt,
    )
    ws.set_row(2, 31)
    headers = ["내부 ID", "그룹", "테스트 항목", "간단한 설명", "시험에서 확인할 것", "적용 조건", "우선순위", "출처 URL"]
    ws.write_row(3, 0, headers, header_fmt)
    ws.set_row(3, 30)
    widths = [15, 20, 27, 46, 50, 22, 10, 38]
    for col, width in enumerate(widths):
        ws.set_column(col, col, width)

    previous_group = None
    for r, test in enumerate(data, start=4):
        group_start = test["group"] != previous_group
        ws.set_row(r, 48)
        values = [
            test["id"],
            test["group"],
            test["name"],
            test["description"],
            test["verify"],
            test["applicability"],
            test["priority"],
            test["source"],
        ]
        for c, value in enumerate(values):
            if c == 1:
                cell_format = group_format(test["group"], center=True, top=group_start)
            elif c in (0, 5, 6):
                cell_format = body_center_fmt
            elif c == 7:
                cell_format = source_fmt
            else:
                cell_format = body_fmt
            if group_start and c != 1:
                top_props = {
                    "text_wrap": True,
                    "valign": "vcenter" if c in (0, 5, 6) else "top",
                    "align": "center" if c in (0, 5, 6) else "left",
                    "border": 1,
                    "border_color": "#E1E7EF",
                    "top": 2,
                    "top_color": COLORS["blue"],
                }
                if c == 7:
                    top_props["font_color"] = "#0563C1"
                    top_props["underline"] = True
                cell_format = fmt(top_props)
            ws.write(r, c, value, cell_format)
        previous_group = test["group"]

    ws.autofilter(3, 0, 3 + len(data), 7)
    ws.print_area(0, 0, 3 + len(data), 6)
    ws.set_row(3 + len(data), 48)
    return ws


summary = workbook.add_worksheet("요약")
summary.hide_gridlines(2)
summary.set_tab_color(COLORS["navy"])
summary.set_column("A:A", 8)
summary.set_column("B:B", 23)
summary.set_column("C:C", 8)
summary.set_column("D:D", 23)
summary.set_column("E:E", 8)
summary.set_column("F:F", 23)
summary.set_column("G:G", 8)
summary.set_column("H:H", 23)
summary.merge_range("A1:H1", "MIPI DSI v1.3.1 CTS — 공개 범위 기반 테스트 정리", title_fmt)
summary.set_row(0, 33)
summary.merge_range(
    "A2:H3",
    "MIPI 공식 페이지가 공개하는 v1.3.1 Receiver Protocol CTS와 Transmitter Protocol CTS 범위를 바탕으로, 공개된 DSI 기능 및 시험장비 coverage를 교차해 만든 실무용 체크리스트입니다. 공식 CTS 원문의 Test ID·Setup·Procedure·Pass/Fail criteria를 전사한 문서가 아니며 인증 판정에는 회원용 원문을 사용해야 합니다.",
    subtitle_fmt,
)
summary.set_row(1, 30)
summary.set_row(2, 30)

cards = [
    ("총 테스트 항목", f"=COUNTA('실행_체크리스트'!$A$5:$A$500)", len(all_items)),
    ("송신기 (Tx)", f'=COUNTIF(\'실행_체크리스트\'!$B$5:$B$500,"송신기 (Tx)")', len(tx)),
    ("수신기 (Rx)", f'=COUNTIF(\'실행_체크리스트\'!$B$5:$B$500,"수신기 (Rx)")', len(rx)),
    ("P0 핵심 항목", f'=COUNTIF(\'실행_체크리스트\'!$H$5:$H$500,"P0")', sum(x["priority"] == "P0" for x in all_items)),
]
for i, (label, formula, cached) in enumerate(cards):
    col = i * 2
    summary.merge_range(4, col, 4, col + 1, label, card_label_fmt)
    summary.merge_range(5, col, 6, col + 1, "", card_value_fmt)
    summary.write_formula(5, col, formula, card_value_fmt, cached)
    summary.set_row(4, 23)
    summary.set_row(5, 28)
    summary.set_row(6, 12)

operational_cards = [
    ("적용 항목", f'=COUNTIF(\'실행_체크리스트\'!$I$5:$I$500,"적용")', sum(x["applicability"] == "공통" for x in all_items)),
    ("완료", f'=COUNTIF(\'실행_체크리스트\'!$J$5:$J$500,"완료")', 0),
    ("Pass", f'=COUNTIF(\'실행_체크리스트\'!$K$5:$K$500,"Pass")', 0),
    ("Fail", f'=COUNTIF(\'실행_체크리스트\'!$K$5:$K$500,"Fail")', 0),
]
for i, (label, formula, cached) in enumerate(operational_cards):
    col = i * 2
    summary.merge_range(8, col, 8, col + 1, label, card_label_fmt)
    summary.merge_range(9, col, 10, col + 1, "", card_value_fmt)
    summary.write_formula(9, col, formula, card_value_fmt, cached)
summary.write(12, 0, "진행률", card_label_fmt)
summary.merge_range("B13:C14", "", percent_fmt)
summary.write_formula(
    "B13",
    '=IF(COUNTIF(\'실행_체크리스트\'!$I$5:$I$500,"적용")=0,0,COUNTIF(\'실행_체크리스트\'!$J$5:$J$500,"완료")/COUNTIF(\'실행_체크리스트\'!$I$5:$I$500,"적용"))',
    percent_fmt,
    0,
)
summary.write_comment(
    "B13",
    "실행_체크리스트에서 ‘적용’으로 지정된 항목 중 상태가 ‘완료’인 항목의 비율입니다.",
    {"author": "OpenAI Codex"},
)
summary.merge_range(
    "D13:H14",
    "적용 여부, 상태, 결과는 ‘실행_체크리스트’에서 선택하세요. 조건부 항목은 기본값이 ‘검토 필요’입니다.",
    note_fmt,
)

summary.merge_range("A16:H16", "그룹별 항목 수", section_fmt)
summary_headers = ["DUT", "그룹", "항목 수", "", "DUT", "그룹", "항목 수", ""]
summary.write_row("A17", summary_headers, header_fmt)
tx_groups = list(dict.fromkeys(x["group"] for x in tx))
rx_groups = list(dict.fromkeys(x["group"] for x in rx))
max_groups = max(len(tx_groups), len(rx_groups))
for idx in range(max_groups):
    row = 17 + idx
    if idx < len(tx_groups):
        group = tx_groups[idx]
        count = sum(x["group"] == group for x in tx)
        summary.write(row, 0, "Tx", body_center_fmt)
        summary.write(row, 1, group, group_format(group, center=False))
        summary.write_formula(
            row,
            2,
            f'=COUNTIFS(\'실행_체크리스트\'!$B$5:$B$500,"송신기 (Tx)",\'실행_체크리스트\'!$C$5:$C$500,B{row + 1})',
            body_center_fmt,
            count,
        )
    if idx < len(rx_groups):
        group = rx_groups[idx]
        count = sum(x["group"] == group for x in rx)
        summary.write(row, 4, "Rx", body_center_fmt)
        summary.write(row, 5, group, group_format(group, center=False))
        summary.write_formula(
            row,
            6,
            f'=COUNTIFS(\'실행_체크리스트\'!$B$5:$B$500,"수신기 (Rx)",\'실행_체크리스트\'!$C$5:$C$500,F{row + 1})',
            body_center_fmt,
            count,
        )
    summary.set_row(row, 24)

scope_start = 19 + max_groups
summary.merge_range(scope_start, 0, scope_start, 7, "범위 해석", section_fmt)
scope_rows = [
    ["포함", "DSI 프로토콜: packet/header/footer, ECC/CRC, command/read/BTA, video mode, pixel packing, LP/HS 관련 protocol sequence"],
    ["조건부", "Virtual Channel, EoTp, ULPS, read response, 특정 pixel format, 압축 등 DUT가 해당 기능을 지원할 때 적용"],
    ["별도 검증", "D-PHY 전기적 특성·eye·jitter·voltage·PHY timing의 정량 합격 기준은 D-PHY CTS 영역으로 이 문서의 주 범위가 아님"],
    ["공식 판정", "회원용 MIPI CTS 원문의 Setup, Procedure, Results/Problems 및 Pass/Fail criteria로 최종 확인"],
]
for offset, row_data in enumerate(scope_rows, start=1):
    r = scope_start + offset
    summary.write(r, 0, row_data[0], card_label_fmt)
    summary.merge_range(r, 1, r, 7, row_data[1], body_fmt)
    summary.set_row(r, 31)
summary.freeze_panes(4, 0)
summary.set_landscape()
summary.set_paper(9)
summary.fit_to_pages(1, 1)
summary.print_area(0, 0, scope_start + len(scope_rows), 7)
summary.set_margins(0.3, 0.3, 0.4, 0.4)


add_detail_sheet(
    "송신기_Tx",
    "MIPI DSI v1.3.1 — 송신기(Host) Protocol 테스트",
    "Host/SoC의 출력 스트림을 분석해 packet 생성, command/video sequence, timing 및 오류 보호가 올바른지 확인하는 관점입니다.",
    tx,
    COLORS["blue"],
)
add_detail_sheet(
    "수신기_Rx",
    "MIPI DSI v1.3.1 — 수신기(Display/Peripheral) Protocol 테스트",
    "시험기가 유효·오류 DSI traffic을 입력하고 Display/Peripheral의 수신, 오류 처리, BTA/read response 및 화면 결과를 확인하는 관점입니다.",
    rx,
    COLORS["green"],
)


checklist = workbook.add_worksheet("실행_체크리스트")
configure_sheet(checklist, COLORS["amber"])
checklist.freeze_panes(4, 3)
checklist.merge_range("A1:O1", "MIPI DSI v1.3.1 — 실행 체크리스트", title_fmt)
checklist.set_row(0, 31)
checklist.merge_range(
    "A2:O2",
    "적용 여부·상태·결과·담당자·증적·비고를 편집해 프로젝트 시험 진행표로 사용할 수 있습니다. 필터와 틀 고정을 적용했습니다.",
    subtitle_fmt,
)
checklist.set_row(1, 38)
checklist.merge_range(
    "A3:O3",
    "조건부 기능은 ‘검토 필요’가 기본값입니다. 제품 capability와 공식 CTS 원문을 대조한 뒤 ‘적용’ 또는 ‘비적용’으로 확정하세요.",
    note_fmt,
)
checklist.set_row(2, 31)
check_headers = [
    "내부 ID", "DUT 역할", "그룹", "테스트 항목", "간단한 설명", "시험에서 확인할 것",
    "적용 조건", "우선순위", "적용 여부", "상태", "결과", "담당자", "증적/로그", "비고", "출처 URL"
]
checklist.write_row(3, 0, check_headers, header_fmt)
checklist.set_row(3, 31)
check_widths = [15, 14, 20, 27, 42, 46, 21, 10, 13, 12, 10, 14, 28, 28, 38]
for col, width in enumerate(check_widths):
    checklist.set_column(col, col, width)

previous_group = None
for r, test in enumerate(all_items, start=4):
    group_start = test["group"] != previous_group or (r == 4 + len(tx))
    checklist.set_row(r, 48)
    applies = "적용" if test["applicability"] == "공통" else "검토 필요"
    values = [
        test["id"], test["dut"], test["group"], test["name"], test["description"], test["verify"],
        test["applicability"], test["priority"], applies, "미실행", "미판정", "", "", "", test["source"]
    ]
    for c, value in enumerate(values):
        if c == 2:
            cell_format = group_format(test["group"], center=True, top=group_start)
        elif c in (0, 1, 6, 7, 8, 9, 10, 11):
            cell_format = body_center_fmt
        elif c == 14:
            cell_format = source_fmt
        else:
            cell_format = body_fmt
        if group_start and c != 2:
            props = {
                "text_wrap": True,
                "valign": "vcenter" if c in (0, 1, 6, 7, 8, 9, 10, 11) else "top",
                "align": "center" if c in (0, 1, 6, 7, 8, 9, 10, 11) else "left",
                "border": 1,
                "border_color": "#E1E7EF",
                "top": 2,
                "top_color": COLORS["blue"],
            }
            if c == 14:
                props["font_color"] = "#0563C1"
                props["underline"] = True
            cell_format = fmt(props)
        checklist.write(r, c, value, cell_format)
    previous_group = test["group"]

first_data_excel = 5
last_data_excel = 4 + len(all_items)
checklist.autofilter(3, 0, 3 + len(all_items), 14)
checklist.data_validation(
    f"I{first_data_excel}:I{last_data_excel}",
    {"validate": "list", "source": ["적용", "비적용", "검토 필요"]},
)
checklist.data_validation(
    f"J{first_data_excel}:J{last_data_excel}",
    {"validate": "list", "source": ["미실행", "진행중", "완료", "보류"]},
)
checklist.data_validation(
    f"K{first_data_excel}:K{last_data_excel}",
    {"validate": "list", "source": ["미판정", "Pass", "Fail", "N/A"]},
)
checklist.conditional_format(
    f"I{first_data_excel}:I{last_data_excel}",
    {"type": "text", "criteria": "containing", "value": "검토 필요", "format": fmt({"bg_color": COLORS["light_amber"], "font_color": "#7F6000"})},
)
checklist.conditional_format(
    f"J{first_data_excel}:J{last_data_excel}",
    {"type": "text", "criteria": "containing", "value": "완료", "format": fmt({"bg_color": COLORS["light_green"], "font_color": "#375623", "bold": True})},
)
checklist.conditional_format(
    f"K{first_data_excel}:K{last_data_excel}",
    {"type": "text", "criteria": "containing", "value": "Pass", "format": fmt({"bg_color": "#C6EFCE", "font_color": "#006100", "bold": True})},
)
checklist.conditional_format(
    f"K{first_data_excel}:K{last_data_excel}",
    {"type": "text", "criteria": "containing", "value": "Fail", "format": fmt({"bg_color": "#FFC7CE", "font_color": "#9C0006", "bold": True})},
)
checklist.print_area(0, 0, 3 + len(all_items), 10)


sources = workbook.add_worksheet("범위_출처")
sources.hide_gridlines(2)
sources.set_tab_color(COLORS["teal"])
sources.set_column("A:A", 14)
sources.set_column("B:B", 24)
sources.set_column("C:C", 52)
sources.set_column("D:D", 62)
sources.set_column("E:E", 35)
sources.set_column("F:F", 15)
sources.merge_range("A1:F1", "범위, 출처 및 용어", title_fmt)
sources.set_row(0, 31)
sources.merge_range(
    "A2:F2",
    "공개 자료만 사용했습니다. MIPI 회원 전용 CTS의 공식 Test ID, 원문 절차와 수치 판정 기준은 포함하지 않았습니다.",
    subtitle_fmt,
)
sources.set_row(1, 38)
sources.merge_range("A4:F4", "출처", section_fmt)
sources.write_row("A5", ["출처 ID", "기관", "공개 자료에서 확인한 내용", "URL", "워크북에서의 사용", "확인일"], header_fmt)
source_rows = [
    ["S1", "MIPI Alliance", "DSI v1.3.1용 Receiver Protocol CTS와 Transmitter Protocol CTS가 별도로 존재하며 회원용임을 확인.", MIPI_URL, "CTS 문서 범위, DSI/D-PHY/DCS/DSC 개요", "2026-07-30"],
    ["S2", "Teledyne LeCroy", "CTS coverage가 data/clock, short/long packet, frame structure, timing, HS/LP 및 read/write를 포함한다고 설명.", TELEDYNE_URL, "공개 coverage를 그룹화하는 보조 근거", "2026-07-30"],
    ["S3", "Synopsys", "packet structure, command/video mode, pixel formats, ECC/CRC, error handling, HS/Escape 및 multi-lane 기능을 공개.", SYNOPSYS_URL, "프로토콜 기능별 체크 항목 보조 근거", "2026-07-30"],
    ["S4", "AMD", "lane 조합, line rate, short/long packet, pixel format, video mode, 오류 복구 등 공개 검증 범위를 설명.", AMD_URL, "구현 검증 및 오류 복구 체크 보조 근거", "2026-07-30"],
]
for r, row in enumerate(source_rows, start=5):
    for c, value in enumerate(row):
        cell_format = source_fmt if c == 3 else (body_center_fmt if c in (0, 1, 5) else body_fmt)
        sources.write(r, c, value, cell_format)
    sources.set_row(r, 57)

scope_row = 11
sources.merge_range(scope_row, 0, scope_row, 5, "포함/제외 범위", section_fmt)
sources.write_row(scope_row + 1, 0, ["구분", "영역", "처리", "이유", "", ""], header_fmt)
scope_table = [
    ["포함", "DSI Protocol Tx/Rx", "테스트 항목으로 정리", "공식 페이지가 v1.3.1 Transmitter/Receiver Protocol CTS를 명시", "", ""],
    ["조건부", "VC, EoTp, read/BTA, ULPS, pixel format, DSC", "지원 기능일 때 적용", "제품별 capability가 다르므로 원문 CTS applicability 확인 필요", "", ""],
    ["별도", "D-PHY 전기/물리 계층", "정량 PHY 시험은 제외", "Protocol CTS와 D-PHY CTS의 목적 및 장비가 다름", "", ""],
    ["대체 불가", "공식 CTS Test ID/절차/판정 기준", "회원용 원문 확인", "공개 페이지에서 세부 문서가 제공되지 않음", "", ""],
]
for r, row in enumerate(scope_table, start=scope_row + 2):
    sources.write(r, 0, row[0], card_label_fmt)
    sources.write(r, 1, row[1], body_fmt)
    sources.write(r, 2, row[2], body_fmt)
    sources.merge_range(r, 3, r, 5, row[3], body_fmt)
    sources.set_row(r, 39)

glossary_row = scope_row + 8
sources.merge_range(glossary_row, 0, glossary_row, 5, "용어", section_fmt)
sources.write_row(glossary_row + 1, 0, ["용어", "설명", "", "", "", ""], header_fmt)
glossary = [
    ["DUT", "Device Under Test. 시험 대상인 Host/SoC 송신기 또는 Display/Peripheral 수신기."],
    ["Short Packet", "고정 길이 header 중심 패킷. 명령, event, 짧은 응답 등에 사용."],
    ["Long Packet", "Word Count, payload와 CRC를 갖는 가변 길이 패킷."],
    ["BTA", "Bus Turn-Around. Host에서 Peripheral 방향으로 버스 구동권을 넘겨 read/ACK 응답을 받는 절차."],
    ["LPDT", "Low-Power Data Transmission. Escape mode에서 수행하는 저전력 데이터 전송."],
    ["EoTp", "End-of-Transmission Packet. 지원 구성에서 전송 종료를 나타내는 short packet."],
    ["P0/P1/P2", "P0=핵심 상호운용성, P1=일반/조건부 기능, P2=선택 기능(예: 압축). 공식 CTS 우선순위 표기가 아님."],
]
for r, row in enumerate(glossary, start=glossary_row + 2):
    sources.write(r, 0, row[0], card_label_fmt)
    sources.merge_range(r, 1, r, 5, row[1], body_fmt)
    sources.set_row(r, 34)

sources.freeze_panes(4, 0)
sources.set_landscape()
sources.set_paper(8)
sources.fit_to_pages(1, 0)
sources.set_margins(0.3, 0.3, 0.4, 0.4)
sources.print_area(0, 0, glossary_row + 1 + len(glossary), 5)

active_sheet = os.environ.get("MIPI_ACTIVE_SHEET", "요약")
active_map = {
    "요약": summary,
    "송신기_Tx": workbook.get_worksheet_by_name("송신기_Tx"),
    "수신기_Rx": workbook.get_worksheet_by_name("수신기_Rx"),
    "실행_체크리스트": checklist,
    "범위_출처": sources,
}
target_sheet = active_map.get(active_sheet, summary)
target_sheet.activate()
if active_sheet != "요약":
    for sheet_name, worksheet in active_map.items():
        if sheet_name != active_sheet:
            worksheet.hide()
workbook.close()
print(f"created={OUTPUT}")
print(f"tx_items={len(tx)}")
print(f"rx_items={len(rx)}")
print(f"total_items={len(all_items)}")
