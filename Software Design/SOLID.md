# SRP Single Responsibility Principle

- Class do only 1 thing
- Small classes/tiny components

# OCP Open-Closed Principle

- Structure should be closed for modification, but open for extensions.
- Once class was written you should not change it. You should be able to expand it.

# LSP Liskov Substitution Principle

- Two types with the same base should be interchangeable. 

Enables you to replace objects of a parent class with objects of a subclass without breaking the application. This requires all subclasses to behave in the same way as the parent class. 

- Don't implement any stricter validation rules on input parameters than implemented by the parent class.
- Apply at the least the same rules to all output parameters as applied by the parent class.

# ISP Interface Segregation Principle

- Keep small interfaces.
- Implement many interfaces if needed.

# DIP Dependency Inversion Principle

- **Use Interfaces or abstract classes**

- High-level modules should not depend on low-level modules. Both should depend on abstractions.
- Abstractions should not depend on details. Details should depend on abstractions.
