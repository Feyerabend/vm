# Virtual Machines


## cmp4

...

## run

Test the sample with:

```shell
> make clean
> make cmp4
```



```ebnf
expression	= term { (+|-) term }

term		= factor { (*|/) factor }

factor		= ident | number | ( expression )
```


#### Expression:
![expression ..](https://user-images.githubusercontent.com/271797/188278982-1ff42147-4e27-490e-ad9f-1b465ed131be.svg)

#### Term:
![term](https://user-images.githubusercontent.com/271797/188279089-32abec43-650d-4acb-9d3c-37bb86bd49fe.svg)

#### Factor:
![factor](https://user-images.githubusercontent.com/271797/188279057-9cc5ec8d-0c7e-4af0-a579-10491d51caf2.svg)

__NOTE: we do not have any identifiers yet, so the "IDENT" in the diagram is not relevant for now.__
