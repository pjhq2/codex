package simple_uvm_pkg;
  import uvm_pkg::*;
  `include "uvm_macros.svh"

  class simple_item extends uvm_sequence_item;
    rand bit [7:0] data;

    `uvm_object_utils_begin(simple_item)
      `uvm_field_int(data, UVM_DEFAULT)
    `uvm_object_utils_end

    function new(string name = "simple_item");
      super.new(name);
    endfunction
  endclass

  class simple_sequence extends uvm_sequence #(simple_item);
    `uvm_object_utils(simple_sequence)

    function new(string name = "simple_sequence");
      super.new(name);
    endfunction

    task body();
      repeat (10) begin
        simple_item req = simple_item::type_id::create("req");
        start_item(req);
        assert(req.randomize());
        finish_item(req);
      end
    endtask
  endclass

  class simple_driver extends uvm_driver #(simple_item);
    `uvm_component_utils(simple_driver)
    virtual simple_if vif;

    function new(string name = "simple_driver", uvm_component parent = null);
      super.new(name, parent);
    endfunction

    function void build_phase(uvm_phase phase);
      super.build_phase(phase);
      if (!uvm_config_db#(virtual simple_if)::get(this, "", "vif", vif))
        `uvm_fatal("NOVIF", "virtual interface was not configured")
    endfunction

    task run_phase(uvm_phase phase);
      vif.drv_cb.valid <= 0;
      vif.drv_cb.data  <= '0;
      wait (vif.rst_n);
      forever begin
        seq_item_port.get_next_item(req);
        vif.drv_cb.valid <= 1;
        vif.drv_cb.data  <= req.data;
        @(vif.drv_cb);
        vif.drv_cb.valid <= 0;
        seq_item_port.item_done();
      end
    endtask
  endclass

  class simple_monitor extends uvm_monitor;
    `uvm_component_utils(simple_monitor)
    virtual simple_if vif;
    uvm_analysis_port #(simple_item) analysis_port;

    function new(string name = "simple_monitor", uvm_component parent = null);
      super.new(name, parent);
      analysis_port = new("analysis_port", this);
    endfunction

    function void build_phase(uvm_phase phase);
      super.build_phase(phase);
      if (!uvm_config_db#(virtual simple_if)::get(this, "", "vif", vif))
        `uvm_fatal("NOVIF", "virtual interface was not configured")
    endfunction

    task run_phase(uvm_phase phase);
      forever begin
        @(vif.mon_cb);
        if (vif.mon_cb.rst_n && vif.mon_cb.valid) begin
          simple_item item = simple_item::type_id::create("item");
          item.data = vif.mon_cb.data;
          analysis_port.write(item);
          `uvm_info("MON", $sformatf("Observed data: 0x%0h", item.data), UVM_MEDIUM)
        end
      end
    endtask
  endclass

  class simple_agent extends uvm_agent;
    `uvm_component_utils(simple_agent)
    uvm_sequencer #(simple_item) sequencer;
    simple_driver                 driver;
    simple_monitor                monitor;

    function new(string name = "simple_agent", uvm_component parent = null);
      super.new(name, parent);
    endfunction

    function void build_phase(uvm_phase phase);
      super.build_phase(phase);
      monitor = simple_monitor::type_id::create("monitor", this);
      if (is_active == UVM_ACTIVE) begin
        sequencer = uvm_sequencer#(simple_item)::type_id::create("sequencer", this);
        driver    = simple_driver::type_id::create("driver", this);
      end
    endfunction

    function void connect_phase(uvm_phase phase);
      if (is_active == UVM_ACTIVE)
        driver.seq_item_port.connect(sequencer.seq_item_export);
    endfunction
  endclass

  class simple_env extends uvm_env;
    `uvm_component_utils(simple_env)
    simple_agent agent;

    function new(string name = "simple_env", uvm_component parent = null);
      super.new(name, parent);
    endfunction

    function void build_phase(uvm_phase phase);
      super.build_phase(phase);
      agent = simple_agent::type_id::create("agent", this);
    endfunction
  endclass

  class simple_test extends uvm_test;
    `uvm_component_utils(simple_test)
    simple_env env;

    function new(string name = "simple_test", uvm_component parent = null);
      super.new(name, parent);
    endfunction

    function void build_phase(uvm_phase phase);
      super.build_phase(phase);
      env = simple_env::type_id::create("env", this);
    endfunction

    task run_phase(uvm_phase phase);
      simple_sequence seq = simple_sequence::type_id::create("seq");
      phase.raise_objection(this);
      seq.start(env.agent.sequencer);
      #20ns;
      phase.drop_objection(this);
    endtask
  endclass
endpackage
