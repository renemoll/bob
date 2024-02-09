Design
======


.. uml::

   actor Developer

   collections Sourcecode

   package Bob {
      collections Tasks
      queue Commands
      component Executor

      Tasks -> Commands
      Commands -> Executor
   }

   file bob.toml
   file CMakeLists.txt
   collections Artifacts

   Developer -> Sourcecode : writes
   Developer --> Bob : invokes

   Tasks <-- bob.toml : configures

   Sourcecode --> Executor : input for
   Executor -> Artifacts : generates
   Executor <-- CMakeLists.txt : configures
