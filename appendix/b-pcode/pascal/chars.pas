program chars(output);
var c: char;
    b: boolean;
begin
    for c := 'a' to 'z' do write(c);
    writeln;
    for c := 'Z' downto 'A' do write(c);
    writeln;
    writeln(ord('A'):1, ' ', chr(97), ' ', succ('m'), pred('n'), ' ', ord(true):1);
    b := 'a' < 'b';
    writeln(b, ' ', not b, ' ', odd(7):6, '|', 'x':3, '|', '''quoted''');
    writeln('a string that is longer than sixteen characters, written in pieces')
end.
