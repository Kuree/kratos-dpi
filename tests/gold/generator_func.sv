import "DPI-C" function shortint test_add(input shortint  a, input shortint  b);
module test (
  input logic [15:0] in,
  output logic [15:0] out
);

always_comb begin
  out = test_add (in, 16'h1);
end
endmodule   // test

