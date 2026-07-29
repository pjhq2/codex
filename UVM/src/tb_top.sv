`timescale 1ns/1ps

module tb_top;
  import uvm_pkg::*;
  import simple_uvm_pkg::*;

  logic clk = 0;
  always #5 clk = ~clk;

  simple_if sif(clk);

  // TODO: 실제 DUT 인스턴스로 교체하세요.
  // dut i_dut (.clk(clk), .rst_n(sif.rst_n), .valid(sif.valid), .data(sif.data));

  initial begin
    sif.rst_n = 0;
    sif.valid = 0;
    sif.data  = '0;
    repeat (2) @(posedge clk);
    sif.rst_n = 1;
  end

  initial begin
    uvm_config_db#(virtual simple_if)::set(null, "uvm_test_top.env.agent.*", "vif", sif);
    run_test("simple_test");
  end
endmodule
