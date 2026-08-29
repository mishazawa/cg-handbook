[Design Patterns](https://refactoring.guru/design-patterns)

Design pattern is a general repeatable solution to a commonly occurring problem in software design. A design pattern isn't a finished design that can be transformed directly into code. It is a description or template for how to solve a problem that can be used in many different situations.

# Creational design patterns

These design patterns are all about class instantiation. This pattern can be further divided into class-creation patterns and object-creational patterns. While class-creation patterns use inheritance effectively in the instantiation process, object-creation patterns use delegation effectively to get the job done.

## Abstract Factory

> The Abstract Factory provides you with an interface for creating objects from each class of the product family. As long as your code creates objects via this interface, you don't have to worry about creating the wrong variant of a product which doesn't match the products already created by your app.

Use the Abstract Factory when your code needs to work with various families of related products, but you don't want it to depend on the concrete classes of those products — they might be unknown beforehand or you simply want to allow for future extensibility.

- Consider implementing the Abstract Factory when you have a class with a set of Factory Methods that blur its primary responsibility.

- In a well-designed program each class is responsible only for one thing. When a class deals with multiple product types, it may be worth extracting its factory methods into a stand-alone factory class or a full-blown Abstract Factory implementation.

## Builder

> Builder is a creational design pattern that lets you construct complex objects step by step. The pattern allows you to produce different types and representations of an object using the same construction code.

The base builder interface defines all possible construction steps, and concrete builders implement these steps to construct particular representations of the product. Meanwhile, the director class guides the order of construction.

The Builder pattern lets you construct products step-by-step. You could defer execution of some steps without breaking the final product. You can even call steps recursively, which comes in handy when you need to build an object tree.

A builder doesn't expose the unfinished product while running construction steps. This prevents the client code from fetching an incomplete result.

- Use the Builder pattern to get rid of a "telescoping constructor".

- Use the Builder to construct Composite trees or other complex objects.

- Use the Builder pattern when you want your code to be able to create different representations of some product (for example, stone and wooden houses).

## Factory Method

> The Factory Method separates product construction code from the code that actually uses the product. Therefore it's easier to extend the product construction code independently from the rest of the code.

- Use the Factory Method when you don't know beforehand the exact types and dependencies of the objects your code should work with.

- Use the Factory Method when you want to provide users of your library or framework with a way to extend its internal components.

- Use the Factory Method when you want to save system resources by reusing existing objects instead of rebuilding them each time. (Object Pool)

## Prototype

> Prototype is a creational design pattern that lets you copy existing objects without making your code dependent on their classes.

- Use the Prototype pattern when your code shouldn't depend on the concrete classes of objects that you need to copy.

- Use the pattern when you want to reduce the number of subclasses that only differ in the way they initialize their respective objects.

- The Prototype pattern is available in C# out of the box with a `ICloneable` interface.

- The prototype can be easily recognized by a `clone` or `copy` methods, etc.

## Singleton

> Singleton is a creational design pattern that lets you ensure that a class has only one instance, while providing a global access point to this instance.

- Use the Singleton pattern when a class in your program should have just a single instance available to all clients; for example, a single database object shared by different parts of the program.

- Use the Singleton pattern when you need stricter control over global variables (DB/Heavy objects(_Flyweight_)).

- Violates the Single Responsibility Principle. The pattern solves two problems at the time (self lifecycle and other functionality).

- The pattern requires special treatment in a multithreaded environment so that multiple threads won't create a singleton object several times.

# Structural design patterns

These design patterns are all about Class and Object composition. Structural class-creation patterns use inheritance to compose interfaces. Structural object-patterns define ways to compose objects to obtain new functionality.

## Adapter

> Adapter is a structural design pattern that allows objects with incompatible interfaces to collaborate.

**`Adapter` provides a different interface to the wrapped object, `Proxy` provides it with the same interface, and `Decorator` provides it with an enhanced interface.**

- Use the Adapter class when you want to use some existing class, but its interface isn't compatible with the rest of your code.

- Use the pattern when you want to reuse several existing subclasses that lack some common functionality that can't be added to the superclass.

- Single Responsibility Principle. You can separate the interface or data conversion code from the primary business logic of the program.

- Open/Closed Principle. You can introduce new types of adapters into the program without breaking the existing client code, as long as they work with the adapters through the client interface.

## Bridge

> Bridge is a structural design pattern that lets you split a large class or a set of closely related classes into two separate hierarchies—abstraction and implementation—which can be developed independently of each other.

- Use the Bridge pattern when you want to divide and organize a monolithic class that has several variants of some functionality (for example, if the class can work with various database servers).

- Use the pattern when you need to extend a class in several orthogonal (independent) dimensions.

- Use the Bridge if you need to be able to switch implementations at runtime.

- You can create platform-independent classes and apps.

- The client code works with high-level abstractions. It isn't exposed to the platform details.

*A pattern isn't just a recipe for structuring your code in a specific way. It can also communicate to other developers the problem the pattern solves.*

## Composite (Object Tree)

> Composite is a structural design pattern that lets you compose objects into tree structures and then work with these structures as if they were individual objects.

The Composite pattern provides you with two basic element types that share a common interface: simple leaves and complex containers. A container can be composed of both leaves and other containers. This lets you construct a nested recursive object structure that resembles a tree.

- Use the Composite pattern when you have to implement a tree-like object structure.

- Use the pattern when you want the client code to treat both simple and complex elements uniformly.

- You can work with complex tree structures more conveniently: use polymorphism and recursion to your advantage.

- Open/Closed Principle. You can introduce new element types into the app without breaking the existing code, which now works with the object tree.

## Decorator (Wrapper)

> Decorator is a structural design pattern that lets you attach new behaviors to objects by placing these objects inside special wrapper objects that contain the behaviors.

The Decorator lets you structure your business logic into layers, create a decorator for each layer and compose objects with various combinations of this logic at runtime. The client code can treat all these objects in the same way, since they all follow a common interface.

- Use the pattern when it's awkward or not possible to extend an object's behavior using inheritance.

- Use the Decorator pattern when you need to be able to assign extra behaviors to objects at runtime without breaking the code that uses these objects.

- You can extend an object's behavior without making a new subclass.
- You can add or remove responsibilities from an object at runtime.
- You can combine several behaviors by wrapping an object into multiple decorators.
- Single Responsibility Principle. You can divide a monolithic class that implements many possible variants of behavior into several smaller classes.
- It's hard to remove a specific wrapper from the wrappers stack.
- It's hard to implement a decorator in such a way that its behavior doesn't depend on the order in the decorators stack.

## Facade

> Facade is a structural design pattern that provides a simplified interface to a library, a framework, or any other complex set of classes.

Often, subsystems get more complex over time. Even applying design patterns typically leads to creating more classes. A subsystem may become more flexible and easier to reuse in various contexts, but the amount of configuration and boilerplate code it demands from a client grows ever larger. The Facade attempts to fix this problem by providing a shortcut to the most-used features of the subsystem which fit most client requirements.

- Use the Facade pattern when you need to have a limited but straightforward interface to a complex subsystem.

- Use the Facade when you want to structure a subsystem into layers.

- You can isolate your code from the complexity of a subsystem.

- A facade can become a god object coupled to all classes of an app.

- Facade defines a simplified interface to a subsystem of objects, but it doesn't introduce any new functionality. The subsystem itself is unaware of the facade. Objects within the subsystem can communicate directly. (Facade and Mediator have similar jobs: they try to organize collaboration between lots of tightly coupled classes.)

## Flyweight (Cache)

> Flyweight is a structural design pattern that lets you fit more objects into the available amount of RAM by sharing common parts of state between multiple objects instead of keeping all of the data in each object.

The benefit of applying the pattern depends heavily on how and where it's used. It's most useful when:

 + an application needs to spawn a huge number of similar objects
 + this drains all available RAM on a target device
 + the objects contain duplicate states which can be extracted and shared between multiple objects

- Use the Flyweight pattern only when your program must support a huge number of objects which barely fit into available RAM.

- The Singleton object can be mutable. Flyweight objects are immutable.

## Proxy

> Proxy is a structural design pattern that lets you provide a substitute or placeholder for another object. A proxy controls access to the original object, allowing you to perform something either before or after the request gets through to the original object.

- Lazy initialization (virtual proxy). This is when you have a heavyweight service object that wastes system resources by being always up, even though you only need it from time to time.

- Access control (protection proxy). This is when you want only specific clients to be able to use the service object; for instance, when your objects are crucial parts of an operating system and clients are various launched applications (including malicious ones).

- Local execution of a remote service (remote proxy). This is when the service object is located on a remote server. In this case, the proxy passes the client request over the network, handling all of the nasty details of working with the network.

- Logging requests (logging proxy). This is when you want to keep a history of requests to the service object.

- Caching request results (caching proxy). This is when you need to cache results of client requests and manage the life cycle of this cache, especially if results are quite large.

- Smart reference. This is when you need to be able to dismiss a heavyweight object once there are no clients that use it. The proxy can keep track of clients that obtained a reference to the service object or its results. From time to time, the proxy may go over the clients and check whether they are still active. If the client list gets empty, the proxy might dismiss the service object and free the underlying system resources.

*`Decorator` and `Proxy` have similar structures, but very different intents. Both patterns are built on the composition principle, where one object is supposed to delegate some of the work to another. The difference is that a `Proxy` usually manages the life cycle of its service object on its own, whereas the composition of `Decorators` is always controlled by the client.*

# Behavioral design patterns

These design patterns are all about Class's objects communication. Behavioral patterns are those patterns that are most specifically concerned with communication between objects.

## Chain of responsibility

> Chain of Responsibility is a behavioral design pattern that lets you pass requests along a chain of handlers. Upon receiving a request, each handler decides either to process the request or to pass it to the next handler in the chain.

- Use the pattern when your program is expected to process different kinds of requests in various ways, but the exact types of requests and their sequences are unknown beforehand. The pattern lets you link several handlers into one chain and, upon receiving a request, "ask" each handler whether it can process it. This way all handlers get a chance to process the request.

- Use the pattern when it's essential to execute several handlers in a particular order. Since you can link the handlers in the chain in any order, all requests will get through the chain exactly as you planned.

- Use the  pattern when the set of handlers and their order are supposed to change at runtime. If you provide setters for a reference field inside the handler classes, you'll be able to insert, remove or reorder handlers dynamically.

- You can control the order of request handling.

- Single Responsibility Principle. You can decouple classes that invoke operations from classes that perform operations.

- Open/Closed Principle. You can introduce new handlers into the app without breaking the existing client code.

- Some requests may end up unhandled.

## Command (Action, Transaction)

> Command is a behavioral design pattern that turns a request into a stand-alone object that contains all information about the request. This transformation lets you pass requests as a method arguments, delay or queue a request's execution, and support undoable operations.

- Use the Command pattern when you want to parametrize objects with operations.

- Use the Command pattern when you want to queue operations, schedule their execution, or execute them remotely.

- Use the Command pattern when you want to implement reversible operations.

- Single Responsibility Principle. You can decouple classes that invoke operations from classes that perform these operations.

- Open/Closed Principle. You can introduce new commands into the app without breaking existing client code.

## Iterator

> Iterator is a behavioral design pattern that lets you traverse elements of a collection without exposing its underlying representation (list, stack, tree, etc.).

The iterator encapsulates the details of working with a complex data structure, providing the client with several simple methods of accessing the collection elements. While this approach is very convenient for the client, it also protects the collection from careless or malicious actions which the client would be able to perform if working with the collection directly.

- Use the Iterator pattern when your collection has a complex data structure under the hood, but you want to hide its complexity from clients (either for convenience or security reasons).

- Use the pattern to reduce duplication of the traversal code across your app.

- Use the Iterator when you want your code to be able to traverse different data structures or when types of these structures are unknown beforehand.

- You can iterate over the same collection in parallel because each iterator object contains its own iteration state.

- For the same reason, you can delay an iteration and continue it when needed.

## Mediator (Intermediary, Controller)

> Mediator is a behavioral design pattern that lets you reduce chaotic dependencies between objects. The pattern restricts direct communications between the objects and forces them to collaborate only via a mediator object.

- Use the Mediator pattern when it's hard to change some of the classes because they are tightly coupled to a bunch of other classes. The pattern lets you extract all the relationships between classes into a separate class, isolating any changes to a specific component from the rest of the components.

- Use the pattern when you can't reuse a component in a different program because it's too dependent on other components. After you apply the Mediator, individual components become unaware of the other components. They could still communicate with each other, albeit indirectly, through a mediator object. To reuse a component in a different app, you need to provide it with a new mediator class.

- Use the Mediator when you find yourself creating tons of component subclasses just to reuse some basic behavior in various contexts.

- Over time a mediator can evolve into a God Object.

*The primary goal of Mediator is to eliminate mutual dependencies among a set of system components. Instead, these components become dependent on a single mediator object. The goal of Observer is to establish dynamic one-way connections between objects, where some objects act as subordinates of others.*

## Memento (Snapshot)

> Memento is a behavioral design pattern that lets you save and restore the previous state of an object without revealing the details of its implementation.

The Memento pattern lets you make full copies of an object's state, including private fields, and store them separately from the object. While most people remember this pattern thanks to the "undo" use case, it's also indispensable when dealing with transactions (i.e., if you need to roll back an operation on error).

- Use the Memento pattern when you want to produce snapshots of the object's state to be able to restore a previous state of the object.

- Use the pattern when direct access to the object's fields/getters/setters violates its encapsulation.

## Observer (Event-Subscriber, Listener)

> Observer is a behavioral design pattern that lets you define a subscription mechanism to notify multiple objects about any events that happen to the object they're observing.

- Use the Observer pattern when changes to the state of one object may require changing other objects, and the actual set of objects is unknown beforehand or changes dynamically.

## State

> State is a behavioral design pattern that lets an object alter its behavior when its internal state changes. It appears as if the object changed its class.

The pattern suggests that you extract all state-specific code into a set of distinct classes. As a result, you can add new states or change existing ones independently of each other, reducing the maintenance cost.

- Use the State pattern when you have an object that behaves differently depending on its current state, the number of states is enormous, and the state-specific code changes frequently.

- Use the pattern when you have a class polluted with massive conditionals that alter how the class behaves according to the current values of the class's fields.

- Use State when you have a lot of duplicate code across similar states and transitions of a condition-based state machine.

## Strategy

> Strategy is a behavioral design pattern that lets you define a family of algorithms, put each of them into a separate class, and make their objects interchangeable.

- Use the pattern when you want to use different variants of an algorithm within an object and be able to switch from one algorithm to another during runtime. The pattern lets you indirectly alter the object's behavior at runtime by associating it with different sub-objects which can perform specific sub-tasks in different ways.

- Use the pattern when you have a lot of similar classes that only differ in the way they execute some behavior. The pattern lets you extract the varying behavior into a separate class hierarchy and combine the original classes into one, thereby reducing duplicate code.

- Use the pattern to isolate the business logic of a class from the implementation details of algorithms that may not be as important in the context of that logic. The pattern lets you isolate the code, internal data, and dependencies of various algorithms from the rest of the code. Various clients get a simple interface to execute the algorithms and switch them at runtime.

- Use the pattern when your class has a massive conditional statement that switches between different variants of the same algorithm. The pattern lets you do away with such a conditional by extracting all algorithms into separate classes, all of which implement the same interface. The original object delegates execution to one of these objects, instead of implementing all variants of the algorithm.

- You can swap algorithms used inside an object at runtime.

- You can isolate the implementation details of an algorithm from the code that uses it.

- You can replace inheritance with composition.

- Open/Closed Principle. You can introduce new strategies without having to change the context.

*A lot of modern programming languages have functional type support that lets you implement different versions of an algorithm inside a set of anonymous functions. Then you could use these functions exactly as you'd have used the strategy objects, but without bloating your code with extra classes and interfaces.*

## Template method

> Template Method is a behavioral design pattern that defines the skeleton of an algorithm in the superclass but lets subclasses override specific steps of the algorithm without changing its structure.

- Use the pattern when you want to let clients extend only particular steps of an algorithm, but not the whole algorithm or its structure.

- Use the pattern when you have several classes that contain almost identical algorithms with some minor differences. As a result, you might need to modify all classes when the algorithm changes. When you turn such an algorithm into a template method, you can also pull up the steps with similar implementations into a superclass, eliminating code duplication. Code that varies between subclasses can remain in subclasses.

- You might violate the `Liskov Substitution Principle` by suppressing a default step implementation via a subclass.

* `Factory Method` is a specialization of `Template Method`. At the same time, a `Factory Method` may serve as a step in a large `Template Method`.*

*`Template Method` is based on inheritance: it lets you alter parts of an algorithm by extending those parts in subclasses. `Strategy` is based on composition: you can alter parts of the object's behavior by supplying it with different strategies that correspond to that behavior. `Template Method` works at the class level, so it's static. `Strategy` works on the object level, letting you switch behaviors at runtime.*

## Visitor

> Visitor is a behavioral design pattern that lets you separate algorithms from the objects on which they operate.

- Use the Visitor when you need to perform an operation on all elements of a complex object structure (for example, an object tree). The Visitor pattern lets you execute an operation over a set of objects with different classes by having a visitor object implement several variants of the same operation, which correspond to all target classes.

- Use the Visitor to clean up the business logic of auxiliary behaviors. The pattern lets you make the primary classes of your app more focused on their main jobs by extracting all other behaviors into a set of visitor classes.

- Use the pattern when a behavior makes sense only in some classes of a class hierarchy, but not in others. You can extract this behavior into a separate visitor class and implement only those visiting methods that accept objects of relevant classes, leaving the rest empty.

- Open/Closed Principle. You can introduce a new behavior that can work with objects of different classes without changing these classes.

- Single Responsibility Principle. You can move multiple versions of the same behavior into the same class.

- A visitor object can accumulate some useful information while working with various objects. This might be handy when you want to traverse some complex object structure, such as an object tree, and apply the visitor to each object of this structure.

- You need to update all visitors each time a class gets added to or removed from the element hierarchy.

- Visitors might lack the necessary access to the private fields and methods of the elements that they're supposed to work with.

*You can treat `Visitor` as a powerful version of the `Command` pattern. Its objects can execute operations over various objects of different classes.* 

*You can use `Visitor` to execute an operation over an entire `Composite` tree.*

*You can use `Visitor` along with `Iterator` to traverse a complex data structure and execute some operation over its elements, even if they all have different classes.*
