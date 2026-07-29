# UVM 기본 템플릿

간단한 요청/응답 신호를 검증하는 SystemVerilog UVM 골격입니다.

## 구성

- `src/simple_if.sv`: DUT 연결용 인터페이스
- `src/simple_uvm_pkg.sv`: 트랜잭션, 시퀀스, 에이전트, 환경, 테스트
- `src/tb_top.sv`: 시뮬레이션 최상위 모듈

`tb_top.sv`의 `dut` 인스턴스는 실제 DUT로 교체하세요. 드라이버의 `valid`, `data` 및 모니터의 샘플링 신호도 DUT 프로토콜에 맞춰 수정하면 됩니다.

## 실행 예시

사용 중인 시뮬레이터에서 UVM 라이브러리를 포함해 아래 순서로 컴파일하세요.

```text
simple_if.sv
simple_uvm_pkg.sv
tb_top.sv
```

