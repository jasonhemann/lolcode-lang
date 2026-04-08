use std::io::File;
use std::hashmap::HashMap;
use std::to_bytes::ToBytes;
use std::vec;

static CODE_LITERAL_LOCATION: u16 = 1;

fn main() {
    compile();
}

mod AccessFlags {
    pub static PUBLIC: u16       = 0x0001;
    pub static PRIVATE: u16      = 0x0002;
    pub static PROTECTED: u16    = 0x0004;
    pub static STATIC: u16       = 0x0008;
    pub static FINAL: u16        = 0x0010;
    pub static SUPER: u16        = 0x0020;
    pub static VOLATILE: u16     = 0x0040;
    pub static TRANSIENT: u16    = 0x0080;
    pub static INTERFACE: u16    = 0x0200;
    pub static ABSTRACT: u16     = 0x0400;
    pub static SYNTHETIC: u16    = 0x1000;
    pub static ANNOTATION: u16   = 0x2000;
    pub static ENUM: u16         = 0x4000;
}

enum CPoolEntry {
    UTF8(~str),                     // value
    INTEGER(i32),                   // value
    FLOAT(f32),                     // value
    LONG(i64),                      // value
    DOUBLE(f64),                    // value
    CLASS(u16),                     // name_ref 
    STRING(u16),                    // content_ref
    FIELD_REF(u16, u16),            // class_ref, name_any_type
    METHOD_REF(u16, u16),           // class_ref, name_and_type
    INTERFACE_METHOD_REF(u16, u16), // class_ref, name_and_type
    NAME_AND_TYPE(u16, u16),        // name_ref, type_ref
    METHOD_HANDLE(u8, u16),         // kind, reference
    METHOD_TYPE(u16),               // descriptor_ref
    INVOKE_DYNAMIC(u16, u16)        // bootstrep_idx, name_and_type
}

#[deriving(IterBytes)]
enum OpCode {
    NOP,
    ACONST_NULL,
    ICONST_M1,
    ICONST_0,
    ICONST_1,
    ICONST_2,
    ICONST_3,
    ICONST_4,
    ICONST_5,
    LCONST_0,
    LCONST_1,
    FCONST_0,
    FCONST_1,
    FCONST_2,
    DCONST_0,
    DCONST_1,
    BIPUSH(u8),
    SIPUSH(u16),
    LDC(u8),
    LDC_W(u16),
    LDC2_W(u16),
    ILOAD(u8),
    LLOAD(u8),
    FLOAD(u8),
    DLOAD(u8),
    ALOAD(u8),
    ILOAD_0,
    ILOAD_1,
    ILOAD_2,
    ILOAD_3,
    LLOAD_0,
    LLOAD_1,
    LLOAD_2,
    LLOAD_3,
    FLOAD_0,
    FLOAD_1,
    FLOAD_2,
    FLOAD_3,
    DLOAD_0,
    DLOAD_1,
    DLOAD_2,
    DLOAD_3,
    ALOAD_0,
    ALOAD_1,
    ALOAD_2,
    ALOAD_3,
    IALOAD,
    LALOAD,
    FALOAD,
    DALOAD,
    AALOAD,
    BALOAD,
    CALOAD,
    SALOAD,
    ISTORE(u8),
    LSTORE(u8),
    FSTORE(u8),
    DSTORE(u8),
    ASTORE(u8),
    ISTORE_0,
    ISTORE_1,
    ISTORE_2,
    ISTORE_3,
    LSTORE_0,
    LSTORE_1,
    LSTORE_2,
    LSTORE_3,
    FSTORE_0,
    FSTORE_1,
    FSTORE_2,
    FSTORE_3,
    DSTORE_0,
    DSTORE_1,
    DSTORE_2,
    DSTORE_3,
    ASTORE_0,
    ASTORE_1,
    ASTORE_2,
    ASTORE_3,
    IASTORE,
    LASTORE,
    FASTORE,
    DASTORE,
    AASTORE,
    BASTORE,
    CASTORE,
    SASTORE,
    POP,
    POP2,
    DUP,
    DUP_X1,
    DUP_X2,
    DUP2,
    DUP2_X1,
    DUP2_X2,
    SWAP,
    IADD,
    LADD,
    FADD,
    DADD,
    ISUB,
    LSUB,
    FSUB,
    DSUB,
    IMUL,
    LMUL,
    FMUL,
    DMUL,
    IDIV,
    LDIV,
    FDIV,
    DDIV,
    IREM,
    LREM,
    FREM,
    DREM,
    INEG,
    LNEG,
    FNEG,
    DNEG,
    ISHL,
    LSHL,
    ISHR,
    LSHR,
    IUSHR,
    LUSHR,
    IAND,
    LAND,
    IOR,
    LOR,
    IXOR,
    LXOR,
    IINC(u8, u8),
    I2L,
    I2F,
    I2D,
    L2I,
    L2F,
    L2D,
    F2I,
    F2L,
    F2D,
    D2I,
    D2L,
    D2F,
    I2B,
    I2C,
    I2S,
    LCMP,
    FCMPL,
    FCMPG,
    DCMPL,
    DCMPG,
    IFEQ(u16),
    IFNE(u16),
    IFLT(u16),
    IFGE(u16),
    IFGT(u16),
    IFLE(u16),
    IF_ICMPEQ(u16),
    IF_ICMPNE(u16),
    IF_ICMPLT(u16),
    IF_ICMPGE(u16),
    IF_ICMPGT(u16),
    IF_ICMPLE(u16),
    IF_ACMPEQ(u16),
    IF_ACMPNE(u16),
    GOTO(u16),
    JSR(u16),
    RET(u8),
    TABLE_SWITCH(TableSwitchData),
    LOOKUP_SWITCH(LookupSwitchData),
    IRETURN,
    LRETURN,
    FRETURN,
    DRETURN,
    ARETURN,
    RETURN,
    GETSTATIC(u16),
    PUTSTATIC(u16),
    GETFIELD(u16),
    PUTFIELD(u16),
    INVOKEVIRTUAL(u16),
    INVOKESPECIAL(u16),
    INVOKESTATIC(u16),
    INVOKEINTERFACE(u16, u8, u8),
    INVOKEDYNAMIC(u16, u8, u8),
    NEW(u16),
    NEWARRAY(u16),
    ANEWARRAY(u16),
    ARRAYLENGTH,
    ATHROW,
    CHECKCAST(u16),
    INSTANCEOF(u16),
    MONITORENTER,
    MONITOREXIT,
    WIDE(WideData),
    MULTIANEWARRAY(u16, u8),
    IFNULL(u16),
    IFNONNULL(u16),
    GOTO_W(u32),
    JSR_W(u32),
    BREAKPOINT,
}

struct TableSwitchData {
    padding: uint,
    default: i32,
    low: i32,
    high: i32,
    jump_offsets: ~[i32]
}

impl IterBytes for TableSwitchData {
    fn iter_bytes(&self, lsb0: bool, f: std::to_bytes::Cb) -> bool {
        let padding = vec::from_elem(self.padding, 0u8);
        let default_bytes = self.default.to_bytes(lsb0);
        let low_bytes = self.low.to_bytes(lsb0);
        let high_bytes = self.high.to_bytes(lsb0);
        let offset_bytes = self.jump_offsets.to_bytes(lsb0);

        f(padding.as_slice())
        && f(default_bytes.as_slice())
        && f(low_bytes.as_slice())
        && f(high_bytes.as_slice())
        && f(offset_bytes.slice_from(8))
    }
}

struct LookupSwitchData {
    padding: uint,
    default: i32,
    n_pairs: i32,
    jump_offsets: ~[(i32, i32)]
}

impl IterBytes for LookupSwitchData {
    fn iter_bytes(&self, lsb0: bool, f: std::to_bytes::Cb) -> bool {
        let padding = vec::from_elem(self.padding, 0u8);
        let default_bytes = self.default.to_bytes(lsb0);
        let n_pairs_bytes = self.n_pairs.to_bytes(lsb0);
        let offset_bytes = self.jump_offsets.to_bytes(lsb0);

        f(padding.as_slice())
        && f(default_bytes.as_slice())
        && f(n_pairs_bytes.as_slice())
        && f(offset_bytes.slice_from(8))
    }
}

enum WideData {
    WIDE_IINC(u16, u16),
    WIDE_LOADSTORE(u8, u16)
}

impl IterBytes for WideData {
    fn iter_bytes(&self, lsb0: bool, f: std::to_bytes::Cb) -> bool {
        match self {
            &WIDE_IINC(idx, const_factor) => {
                let idx_bytes = idx.to_bytes(lsb0);
                let const_bytes = const_factor.to_bytes(lsb0);
                
                f(&[0x84]) &&
                f(idx_bytes.as_slice()) && 
                f(const_bytes.as_slice())
            },
            &WIDE_LOADSTORE(opcode, idx)  => {
                let idx_bytes = idx.to_bytes(lsb0);

                f(&[opcode]) &&
                f(idx_bytes.as_slice())
            }
        }
    }
}



struct CPool {
    entries: ~[CPoolEntry],
    next_idx: u16,
    kv_map: ~HashMap<uint, u16>,
    vk_map: ~HashMap<u16, uint>
}

impl CPool {
    fn new() -> CPool {
        CPool {
            entries: ~[], next_idx: 1, 
            kv_map: ~HashMap::<uint, u16>::new(), 
            vk_map: ~HashMap::<u16, uint>::new()
        }
    }

    fn add_entry(&mut self, entry: CPoolEntry) -> u16 {
        let increment = match entry {
            LONG(_) | DOUBLE(_) => 2,
            _                   => 1
        };

        self.entries.push(entry);
        self.kv_map.insert(self.entries.len() - 1, self.next_idx);
        self.vk_map.insert(self.next_idx, self.entries.len() - 1);
        self.next_idx += increment;

        // Return the idx of the added entry
        self.next_idx - increment
    }

    fn get<'a>(&'a self, idx: uint) -> &'a CPoolEntry {
        &self.entries[idx]
    }

    fn vec_to_pool<'a>(&'a self, vec_idx: &uint) -> &'a u16 {
        self.kv_map.get(vec_idx)
    }

    fn pool_to_vec<'a>(&'a self, pool_idx: &u16) -> &'a uint {
        self.vk_map.get(pool_idx)
    }

    fn to_vec(&self) -> ~[u8] {
        let mut buf = ~[];

        buf.push_all(self.next_idx.to_bytes(false));

        for entry in self.entries.iter() {
            match entry {
                &UTF8(ref val)  => {
                    buf.push(1);
                    buf.push_all((val.len() as u16).to_bytes(false));
                    let str_bytes = val.to_bytes(false);
                    buf.push_all(str_bytes.slice(0, str_bytes.len() - 1));
                },
                &INTEGER(val)   => {
                    buf.push(3);
                    buf.push_all(val.to_bytes(false));
                },
                &FLOAT(val)     => {
                    buf.push(4);
                    buf.push_all(val.to_bytes(false));
                },
                &LONG(val)      => {
                    buf.push(5);
                    buf.push_all(val.to_bytes(false));
                },
                &DOUBLE(val)    => {
                    buf.push(6);
                    buf.push_all(val.to_bytes(false));
                },
                &CLASS(ref_idx) => {
                    buf.push(7);
                    buf.push_all(ref_idx.to_bytes(false));
                },
                &STRING(ref_idx) => {
                    buf.push(8);
                    buf.push_all(ref_idx.to_bytes(false));
                },
                &FIELD_REF(class_ref, name_and_type) => {
                    buf.push(9);
                    buf.push_all(class_ref.to_bytes(false));
                    buf.push_all(name_and_type.to_bytes(false));
                },
                &METHOD_REF(class_ref, name_and_type) => {
                    buf.push(10);
                    buf.push_all(class_ref.to_bytes(false));
                    buf.push_all(name_and_type.to_bytes(false));
                },
                &INTERFACE_METHOD_REF(class_ref, name_and_type) => {
                    buf.push(11);
                    buf.push_all(class_ref.to_bytes(false));
                    buf.push_all(name_and_type.to_bytes(false));
                },
                &NAME_AND_TYPE(name_ref, type_ref) => {
                    buf.push(12);
                    buf.push_all(name_ref.to_bytes(false));
                    buf.push_all(type_ref.to_bytes(false));
                },
                &METHOD_HANDLE(kind, ref_idx) => {
                    buf.push(15);
                    buf.push(kind);
                    buf.push_all(ref_idx.to_bytes(false));
                },
                &METHOD_TYPE(descriptor_ref) => {
                    buf.push(16);
                    buf.push_all(descriptor_ref.to_bytes(false));
                },
                &INVOKE_DYNAMIC(bootstrap_idx, name_and_type) => {
                    buf.push(18);
                    buf.push_all(bootstrap_idx.to_bytes(false));
                    buf.push_all(name_and_type.to_bytes(false));
                }
            }
        };

        buf
    }
}


struct Method {
    accflags: u16,
    name_idx: u16,
    desc_idx: u16,
    code: CodeAttr
}

impl Method {
    fn new(name_idx: u16, desc_idx: u16) -> Method {
        Method {
            accflags: 0,
            name_idx: name_idx,
            desc_idx: desc_idx,
            code: CodeAttr::new()
        }
    }

    fn set_accflags(&mut self, flags: u16) {
        self.accflags = flags;
    }

    fn add_accflags(&mut self, flags: u16) {
        self.accflags |= flags;
    }

    fn get_immut_code<'a>(&'a self) -> &'a CodeAttr {
        &self.code
    }

    fn get_code<'a>(&'a mut self) -> &'a mut CodeAttr {
        &mut self.code
    }

    fn to_vec(&self) -> ~[u8] {
        let mut buf = ~[];

        buf.push_all(self.accflags.to_bytes(false));
        buf.push_all(self.name_idx.to_bytes(false));
        buf.push_all(self.desc_idx.to_bytes(false));
        buf.push(0); buf.push(1);   // 1 code attr

        buf.push_all(CODE_LITERAL_LOCATION.to_bytes(false));
        let code_vec = self.code.to_vec();

        buf.push_all((code_vec.len() as u32).to_bytes(false));
        buf.push_all(code_vec);

        buf
    }
}


struct CodeAttr {
    max_stack: u16,
    max_locals: u16,
    code: ~[OpCode]
}

impl CodeAttr {
    fn new() -> CodeAttr {
        CodeAttr {
            max_stack: 0,
            max_locals: 0,
            code: ~[]
        }
    }

    fn inc_max_stack(&mut self) {
        self.max_stack += 1;
    }

    fn inc_max_locals(&mut self) {
        self.max_locals += 1;
    }

    fn to_vec(&self) -> ~[u8] {
        let mut buf = ~[];
        buf.push_all(self.max_stack.to_bytes(false));
        buf.push_all(self.max_locals.to_bytes(false));

        let mut code_bytes = ~[];
        for opcode in self.code.iter() {
            let op_bytes = opcode.to_bytes(false);
            code_bytes.push_all(op_bytes.slice_from(7));
        };

        buf.push_all((code_bytes.len() as u32).to_bytes(false));
        buf.push_all(code_bytes);

        buf.push(0); buf.push(0); // No exception handler so far
        buf.push(0); buf.push(0); // No attributes
        buf
    }

    fn push_opcode<'a>(&'a mut self, opcode: OpCode) -> &'a mut CodeAttr {
        self.code.push(opcode);
        self
    }
}


struct Field {
    access_flags: u16,
    name_idx: u16,
    desc_idx: u16
}

impl Field {
    fn new(name_idx: u16, desc_idx: u16) -> Field {
        Field {
            access_flags: 0,
            name_idx: name_idx,
            desc_idx: desc_idx
        }
    }

    fn add_accflags(&mut self, accflags: u16) {
        self.access_flags |= accflags
    }

    fn set_accflags(&mut self, accflags: u16) {
        self.access_flags = accflags
    }

    fn to_vec(&self) -> ~[u8] {
        let mut buf = ~[];

        buf.push_all(self.access_flags.to_bytes(false));
        buf.push_all(self.name_idx.to_bytes(false));
        buf.push_all(self.desc_idx.to_bytes(false));
        buf.push(0); buf.push(0);   // Not attributes

        buf
    }
}


struct ClassFile {
    major: u16,
    minor: u16,
    cpool: CPool,
    this_class: u16,
    super_class: u16,
    access_flags: u16,
    interfaces: ~[u16],
    fields: ~[Field],
    methods: ~[Method],
}

impl ClassFile {
    fn new(major: u16, minor: u16, this_class: ~str, super_class: ~str) -> ClassFile {
        
        let mut pool = CPool::new();
        pool.add_entry(UTF8(~"Code"));  // Always have the code attribute first
        
        let this_class_name_idx = pool.add_entry(UTF8(this_class));
        let super_class_name_idx = pool.add_entry(UTF8(super_class));
        
        let this_class_idx = pool.add_entry(CLASS(this_class_name_idx));
        let super_class_idx = pool.add_entry(CLASS(super_class_name_idx));

        ClassFile {
            major: major,
            minor: minor,
            cpool: pool,
            this_class: this_class_idx,
            super_class: super_class_idx,
            access_flags: 0,
            interfaces: ~[],
            fields: ~[],
            methods: ~[],
        }
    }

    fn get_cpool<'a>(&'a mut self) -> &'a mut CPool {
        &mut self.cpool
    }

    fn get_immut_cpool<'a>(&'a self) -> &'a CPool {
        &self.cpool
    }

    fn add_accflags(&mut self, accflags: u16) {
        self.access_flags |= accflags;
    }

    fn set_accflags(&mut self, accflags: u16) {
        self.access_flags = accflags;
    }

    fn add_interface(&mut self, idx: u16) {
        self.interfaces.push(idx)
    }

    fn add_field(&mut self, field: Field) {
        self.fields.push(field);
    }

    fn add_method(&mut self, method: Method) {
        self.methods.push(method);
    }

    fn to_vec(&self) -> ~[u8] {
        let mut buf = ~[];

        buf.push_all(0xCAFEBABEu32.to_bytes(false));
        buf.push_all(self.minor.to_bytes(false));
        buf.push_all(self.major.to_bytes(false));

        buf.push_all(self.cpool.to_vec());

        buf.push_all(self.access_flags.to_bytes(false));
        buf.push_all(self.this_class.to_bytes(false));
        buf.push_all(self.super_class.to_bytes(false));

        buf.push_all((self.interfaces.len() as u16).to_bytes(false));
        for idx in self.interfaces.iter() {
            buf.push_all(idx.to_bytes(false));
        }

        buf.push_all((self.fields.len() as u16).to_bytes(false));
        for field in self.fields.iter() {
            buf.push_all(field.to_vec());
        }

        buf.push_all((self.methods.len() as u16).to_bytes(false));
        for method in self.methods.iter() {
            buf.push_all(method.to_vec());
        }

        buf.push(0); buf.push(0);   // No attributes

        buf
    }
}



fn compile() {

    let minor = 0;
    let major = 51;
    let mut cf = ClassFile::new(major, minor, ~"CompilerTest", ~"java/lang/Object");
    cf.set_accflags(AccessFlags::PUBLIC | AccessFlags::SUPER);


    let init_name_idx;
    let init_sig_idx;
    let main_name_idx;
    let main_sig_idx;
    let init_name_and_type;
    let init_ref;

    {    
        let cpool = cf.get_cpool();
        init_name_idx = cpool.add_entry(UTF8(~"<init>"));
        init_sig_idx = cpool.add_entry(UTF8(~"()V"));
        main_name_idx = cpool.add_entry(UTF8(~"main"));
        main_sig_idx = cpool.add_entry(UTF8(~"([Ljava/lang/String;)V"));
        init_name_and_type = cpool.add_entry(NAME_AND_TYPE(init_name_idx, init_sig_idx));
        init_ref = cpool.add_entry(METHOD_REF(cf.super_class, init_name_and_type));
    }

    // Method 1: <init>
    let mut init = Method::new(init_name_idx, init_sig_idx);
    init.get_code().inc_max_locals();
    init.get_code().inc_max_stack();
    init.get_code()
        .push_opcode(ALOAD_0)
        .push_opcode(INVOKESPECIAL(11))
        .push_opcode(RETURN);

    cf.add_method(init);

    // Method 2: main
    let mut main = Method::new(main_name_idx, main_sig_idx);
    main.set_accflags(AccessFlags::PUBLIC | AccessFlags::STATIC);
    main.get_code().inc_max_locals();
    main.get_code().inc_max_stack();
    main.get_code().push_opcode(RETURN);

    cf.add_method(main);


    let mut file = File::create(&Path::new("CompilerTest.class"));
    file.write(cf.to_vec());
    file.flush();
}