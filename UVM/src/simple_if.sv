interface simple_if(input logic clk);
  logic       rst_n;
  logic       valid;
  logic [7:0] data;

  clocking drv_cb @(posedge clk);
    default input #1step output #0;
    output valid, data;
  endclocking

  clocking mon_cb @(posedge clk);
    default input #1step output #0;
    input rst_n, valid, data;
  endclocking
endinterface
