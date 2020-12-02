grammar PolyBot;

root : (line '\n'+)+ EOF;

line : assign | printl | comment | colorl | areal | perimeterl | verticesl | insidel | drawl;

assign: identifier ':=' LEFT_SQUARE point* RIGHT_SQUARE;

printl: 'print' ((QMARK string QMARK)|identifier);
comment: '//' string;
colorl: 'color' identifier ',' LEFT_BRACE color RIGHT_BRACE;
areal: 'area' identifier;
perimeterl: 'perimeter' identifier;
verticesl: 'vertices' identifier;
insidel: 'inside' identifier identifier;
drawl: 'draw' QMARK filename QMARK (',' identifier)+;

point: NUM NUM;
color: NUM NUM NUM;

string: ~('\r'|'\n')*;

filename: FNAME;
identifier: VALID_ID;

FNAME: (DIGIT|LETTER)+ EXT;
VALID_ID: LETTER (DIGIT|LETTER)*;

NUM: MINUS? DIGIT+ ('.' DIGIT+)?;
MINUS: '-';
DIGIT : [0-9] ;
LETTER : [a-zA-Z] ;
LEFT_SQUARE : '[' ;
RIGHT_SQUARE : ']' ;
LEFT_BRACE : '{' ;
RIGHT_BRACE : '}' ;
QMARK: '"';
DOT: '.';
EXT: '.png';
WS : [ \t]+ -> skip;