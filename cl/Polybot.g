grammar PolyBot;

root : (line (EOF | '\n'+))+ EOF;

line : assign | printl | comment | colorl | areal | perimeterl | verticesl | insidel | drawl | regularl | expr | equall | centroidl;


expr: expr INTERSECTION expr | expr UNION expr | BBOX expr | identifier | pointlist | RAND integer;
pointlist: LEFT_SQUARE point* RIGHT_SQUARE;
assign: identifier ':=' expr;

printl: 'print' ((QMARK string QMARK)|expr);
comment: '//' string;
colorl: 'color' identifier ',' LEFT_BRACE color RIGHT_BRACE;
areal: 'area' expr;
perimeterl: 'perimeter' expr;
verticesl: 'vertices' expr;
insidel: 'inside' expr ',' expr;
drawl: 'draw' QMARK filename QMARK (',' expr)+;
regularl: 'regular' expr;
equall: 'equal' expr ',' expr;
centroidl: 'centroid' expr;


point: NUM NUM;
color: NUM NUM NUM;

string: ~('\r'|'\n')*;

filename: FNAME;
identifier: VALID_ID;
integer: INT;

FNAME: (DIGIT|LETTER)+ EXT;
VALID_ID: LETTER (DIGIT|LETTER)*;

INT: DIGIT+;
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
INTERSECTION: '*';
UNION: '+';
BBOX: '#';
RAND: '!';
WS : [ \t]+ -> skip;