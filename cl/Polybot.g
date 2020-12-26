grammar PolyBot;

root : (line comment? (EOF | '\n'+))+ EOF;

line : assign | printl | comment | colorl | areal | perimeterl | verticesl | insidel | drawl | regularl | equall | centroidl;

/*
TODO: Parentesis en expr
*/
expr: LEFT_PAREN expr RIGHT_PAREN| expr INTERSECTION expr | expr UNION expr | BBOX expr | identifier | pointlist | RAND NUM;
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

FNAME: (DIGIT|LETTER)+ '.png';
VALID_ID: LETTER (DIGIT|LETTER)*;

NUM: MINUS? DIGIT+ ('.' DIGIT+)?;
DIGIT : [0-9] ;

MINUS: '-';
LETTER : [a-zA-Z] ;
LEFT_SQUARE : '[' ;
RIGHT_SQUARE : ']' ;
LEFT_BRACE : '{' ;
RIGHT_BRACE : '}' ;
LEFT_PAREN: '(';
RIGHT_PAREN: ')';
QMARK: '"';
DOT: '.';
INTERSECTION: '*';
UNION: '+';
BBOX: '#';
RAND: '!';
WS : [ \t]+ -> skip;