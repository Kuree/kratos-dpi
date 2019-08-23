import "DPI-C" function int test_a(input int a, input int b);

module raw_function(input logic a, output logic b);

assign b = test_a(1, a);

endmodule
